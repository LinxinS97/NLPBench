import os
import json
import traceback
from typing import Optional
from collections import Counter
from utils import ApiManager, PromptGenerator, tot_solver


class Solver:
    def __init__(
            self,
            data_path: str,
            model_name: str,
            seed: int,
            shot_type: str,
            prompt_r: str,
            sys: bool,
            max_tokens: int,
            ctx: bool,
            self_consistency: bool = False,
            self_reflection: bool = False,
    ):
        self.data_path = data_path
        self.model_name_save = model_name.split('/')[-1]
        ctx_path = 'ctx' if ctx else 'no_ctx'
        self.save_path = (f'res/{str(seed)}/{ctx_path}/{shot_type}'
                          f'{"-sc" if self_consistency else ""}'
                          f'_{self.model_name_save}'
                          f'{("_" + prompt_r) if prompt_r is not None else ""}'
                          f'{"_sys" if sys else ""}.json')

        root = self.save_path.rsplit('/', 1)[0]
        if not os.path.exists(root):
            os.makedirs(root)

        self.ctx = ctx

        ### Init api manager and prompt generator
        self.llm = ApiManager(
            model_name=model_name,
            seed=seed,
            default_max_tokens=max_tokens,
        )

        self.prompt = PromptGenerator(
            api=self.llm,
            system_prompt=sys,
            shot_type=shot_type,
            prompt_reinforcement=prompt_r,
        )

        self.self_consistency = self_consistency
        self.self_reflection = self_reflection

    @staticmethod
    def load_cache(save_path: str):
        skip_cnt = 0
        res_cache = []
        if os.path.exists(save_path):
            res_cache = json.load(open(save_path, 'r'))
            skip_cnt = len(res_cache)

        return res_cache, skip_cnt

    @staticmethod
    def majority_voting(resp_list: list):
        res = [r.replace(' ', '').replace("'", '').replace('"', '') for r in resp_list]
        res = Counter(res).most_common(1)[0][0]
        return res

    def solve_ctx(self):
        ### Load cache (if palm, else init result)
        if self.llm.api_type == 'palm':
            res, skip_cnt = self.load_cache(self.save_path)
        else:
            res = []
            skip_cnt = 0

        for data in json.load(open(self.data_path, 'r')):
            if skip_cnt > 0:
                skip_cnt -= 1
                continue
            history = None
            resps = []
            for idx, q in enumerate(data['questions']):
                q_type = data['type'][idx]
                q_opt = [] if data['options'][idx] is None else data['options'][idx]
                ctx = None if data['context'] == '-1' else data['context']
                messages = self.prompt.generate(q=q, q_type=q_type, q_opt=q_opt, ctx=ctx, history=history)

                if self.self_consistency is True and q_type == 0:
                    try:
                        resp = self.llm(messages, choices=3)
                        if resp is None:
                            resp = ""
                    except Exception as e:
                        print(e)
                        resp = ""
                    if resp != "":
                        resp = self.majority_voting(resp)
                else:
                    try:
                        resp = self.llm(messages)
                        if resp is None:
                            resp = ""
                    except Exception as e:
                        print(e)
                        resp = ""

                if self.llm.api_type == 'palm':
                    history = messages
                    history['prompt'] += '\n' + resp

                elif self.llm.api_type == 'oai':
                    history = messages
                    history[-1]['content'] += resp
                resps.append(resp)
                print(f"\n{self.model_name_save}: {resp}")

            res.append({
                **data,
                'prompt': history,
                'llm_answer': resps
            })
            if self.llm.api_type == 'palm':
                json.dump(res, open(self.save_path, 'w'), indent=4)

        json.dump(res, open(self.save_path, 'w'), indent=4)

    def solve_no_ctx(self):
        ### Load cache (if palm, else init result)
        if self.llm.api_type == 'palm':
            res, skip_cnt = self.load_cache(self.save_path)
        else:
            res = []
            skip_cnt = 0

        for data in json.load(open(self.data_path, 'r')):
            if skip_cnt > 0:
                skip_cnt -= 1
                continue
            q = data['question']
            q_type = data['type']
            q_opt = data.get('options', [])

            messages = self.prompt.generate(q=q, q_type=q_type, q_opt=q_opt)
            if q_type == 0 and self.self_consistency is True:
                try:
                    resp = self.llm(messages, choices=3)
                except Exception as e:
                    traceback.print_exc()
                    messages = []
                    resp = ""
                if resp != "":
                    resp = self.majority_voting(resp)
            else:
                try:
                    resp = self.llm(messages)
                except Exception as e:
                    traceback.print_exc()
                    messages = []
                    resp = ""
            print(f"\n {self.model_name_save}: {resp}")
            res.append({
                **data,
                'prompt': messages,
                'llm_answer': resp
            })
            if self.llm.api_type == 'palm':
                json.dump(res, open(self.save_path, 'w'), indent=4)

        json.dump(res, open(self.save_path, 'w'), indent=4)

    def solve_tot_no_ctx(
            self,
            evaluation_strategy: Optional[str] = "vote",  # value or vote
            num_thoughts: Optional[int] = 1,
            max_steps: Optional[int] = 3,
            max_states: Optional[int] = 4,
            pruning_threshold: Optional[float] = 0.5,
    ):
        ### Load cache (if palm, else init result)
        if self.llm.api_type == 'palm':
            res, skip_cnt = self.load_cache(self.save_path)
        else:
            res = []
            skip_cnt = 0

        for data in json.load(open(self.data_path, 'r')):
            if skip_cnt > 0:
                skip_cnt -= 1
                continue
            try:
                resp, messages = tot_solver(
                    generator=self.prompt,
                    api=self.llm,
                    q=data['question'],
                    q_type=data['type'],
                    q_opt=data.get('options', []),
                    evaluation_strategy=evaluation_strategy,
                    num_thoughts=num_thoughts,
                    max_steps=max_steps,
                    max_states=max_states,
                    pruning_threshold=pruning_threshold,
                )
            except Exception as e:
                traceback.print_exc()
                messages = []
                resp = ""

            print(f"\n {self.model_name_save}: {resp}")
            res.append({
                **data,
                'messages': messages,
                'llm_answer': resp
            })
            if self.llm.api_type == 'palm':
                out_str = json.dumps(res[-1])
                with open(self.save_path, 'a') as f:
                    f.write(out_str + '\n')

        json.dump(res, open(self.save_path, 'w'), indent=4)

    def run(self):
        if self.ctx:
            self.solve_ctx()
        else:
            if self.prompt.prompt_reinf == 'tot':
                self.solve_tot_no_ctx()
            else:
                self.solve_no_ctx()
