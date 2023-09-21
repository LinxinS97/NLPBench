import logging
import concurrent.futures
import os
import json
import numpy as np
from typing import List, Dict, Any, Optional, Union
from utils import ApiManager, PromptGenerator
from prompts import SOLUTION_PROMPT, STATE_PROMPT, VOTE_PROMPT


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



class ToTModel:

    api: ApiManager
    evaluation_strategy: Optional[str] = "value"

    def __init__(self, api: ApiManager, evaluation_strategy: Optional[str] = "value"):
        self.api = api
        self.evaluation_strategy = evaluation_strategy


    def message_handler(self, message: str):
        if self.api.api_type == 'palm':
            return {
                'prompt': message,
            }
        elif self.api.api_type == 'oai':
            return [{
                'role': 'user',
                'content': message,
            }]


    def generate_thoughts(self, 
                          state: Union[str, list], 
                          k: int, 
                          initial_prompt: Union[str, dict], 
                          rejected_solutions: Optional[str]=None):
        
        if type(state) == str:
            state_text = state
        else:
            state_text = '\n'.join(state)

        prompt = SOLUTION_PROMPT.format(state_text=state_text,
                                        initial_prompt=initial_prompt, 
                                        rejected_solutions=rejected_solutions)
        
        prompt = self.message_handler(prompt)
        thoughts = [self.api(prompt) for _ in range(k)]
        return thoughts

        
    def generate_solution(self, 
                          initial_prompt: str, 
                          state: Union[str, list], 
                          rejected_solutions: Optional[str]=None):
        try:
            if type(state) == str:
                state_text = state
            else:
                state_text = '\n'.join(state)
            
            prompt = SOLUTION_PROMPT.format(state_text=state_text,
                                            initial_prompt=initial_prompt, 
                                            rejected_solutions=rejected_solutions)
            prompt = self.message_handler(prompt)
            answer = self.api(prompt)
            return answer
        
        except Exception as e:
            logger.error(f"Error in generate_solutions: {e}")
            return None


    def evaluate_states(self, 
                        states: List, 
                        initial_prompt: str):
        if not states:
            return {}

        if self.evaluation_strategy == 'value':
            state_values = {}
            for state in states:
                if type(state) == str:
                    state_text = state
                else:
                    state_text = '\n'.join(state)

                prompt = STATE_PROMPT.format(initial_prompt=initial_prompt, state_text=state_text)
                prompt = self.message_handler(prompt)
                try:
                    value_text = self.api(prompt, 10)
                    value = float(value_text)
                    print(f"Evaluated Thought Value: {value}")
                except ValueError:
                    value = 0  # Assign a default value if the conversion fails
                state_values[state] = value
            return state_values

        elif self.evaluation_strategy == 'vote':
            states_text = '\n'.join([' '.join(state) for state in states])

            prompt = VOTE_PROMPT.format(states_text=states_text, initial_prompt=initial_prompt)
            prompt = self.message_handler(prompt)
            best_state_text = self.api(prompt, 50)

            best_state = tuple(best_state_text.split())

            return {state: 1 if state == best_state else 0 for state in states}
        
        else:
            raise ValueError("Invalid evaluation strategy. Choose 'value' or 'vote'.")



class TreeofThoughts:

    model: ToTModel
    best_state = None
    best_value = float("-inf")
    history = [] #added line initalize history
    tree: Dict[str, Dict[str, Union[float, Dict[str, Any]]]] = {
        "nodes": {},
    }

    def __init__(self, model: ToTModel):
        self.model = model

    def save_tree_to_json(self, file_name):
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, 'w') as json_file:
            json.dump(self.tree, json_file, indent=4)

    def logNewState(self, state, evaluation):
        if not (type(state) == str):
            state = " | ".join(state)
        if state in self.tree['nodes']:
            self.tree['nodes'][state]['thoughts'].append(evaluation)
        else:
            self.tree['nodes'][state] = {'thoughts': [evaluation]}

    def adjust_pruning_threshold_precentile(self, evaluated_thoughts, percentile):
        values = np.array(list(evaluated_thoughts.values()))
        if values.size == 0:
            return 0 
        return max(np.percentile(values, percentile), 0.1)
    

    def adjust_pruning_threshold_moving_average(self, evaluated_thoughts, window_size):
        values = list(evaluated_thoughts.values())
        if len(values) < window_size:
            return np.mean(values) if values else 0
        else:
            return max(np.mean(values[-window_size:]), 0.1)



class TreeofThoughtsBFS(TreeofThoughts):
    def solve(
        self, 
        initial_prompt, 
        num_thoughts, 
        max_steps, 
        max_states, 
        pruning_threshold=0.5
    ):
        current_states = [initial_prompt]
        state_values = {}
        dynamic_pruning_threshold = pruning_threshold

        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for _ in range(1, max_steps + 1):
                    selected_states = []
                    for state in current_states:
                        thoughts = self.model.generate_thoughts(state, num_thoughts, initial_prompt)
                        futures = [executor.submit(self.model.evaluate_states, {thought: 0}, initial_prompt) for thought in thoughts]
                        concurrent.futures.wait(futures)
                        evaluated_thoughts = {thought: list(fut.result().values()) for thought, fut in zip(thoughts, futures)}

                        if evaluated_thoughts:  # only adjust if you have evaluated thoughts
                            dynamic_pruning_threshold = self.adjust_pruning_threshold_moving_average(evaluated_thoughts, 5)

                        for thought, value in evaluated_thoughts.items():
                            flattened_state = (state, thought) if isinstance(state, str) else (*state, thought)
                            selected_states.append((flattened_state, value))

                        selected_states.sort(key=lambda x: x[1], reverse=True)
                        selected_states = selected_states[:max_states]  # Select only the top states

                        for state, value in selected_states:
                            if value >= dynamic_pruning_threshold:
                                state_values[state] = value
                                self.logNewState(state, value)
                                logger.debug(f"State Values: {state_values}")

            if state_values:
                highest_rated_solution = max(state_values.items(), key=lambda x: x[1])
                highest_rated_state = highest_rated_solution[0]
                solution = self.model.generate_solution(initial_prompt, highest_rated_state)

                return solution, highest_rated_state

            else:
                return None

        except Exception as e:
            logger.error(f"Error in tot_bfs: {e}")
            return None



def tot_solver(
    generator: PromptGenerator,
    api: ApiManager,
    q: str,
    q_type: int,
    q_opt: Optional[List[str]] = [],
    evaluation_strategy: Optional[str] = "vote",  # value or vote
    num_thoughts: Optional[int] = 1,
    max_steps: Optional[int] = 3,
    max_states: Optional[int] = 4,
    pruning_threshold: Optional[float] = 0.5,
):
    tot_model = ToTModel(api, evaluation_strategy)
    tot = TreeofThoughtsBFS(tot_model)
    initial_prompt = generator.generate(q, q_type, q_opt)

    if generator.api_type == 'palm':
        input_prompt = initial_prompt['prompt']
    else:
        input_prompt = initial_prompt[-1]['content']

    resp = tot.solve(
        initial_prompt=input_prompt,
        num_thoughts=num_thoughts,
        pruning_threshold=pruning_threshold,
        max_steps=max_steps,
        max_states=max_states
    )

    return resp

