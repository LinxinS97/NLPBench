import os
import time

import google.generativeai as palm
from flaml import autogen
from typing import List, Optional, Union
from prompts import SYS_PROMPT_MAPPING, PROMPT_MAPPING, SHORTANS_ZS_COT_ST1


palm.configure(api_key=os.environ.get("PALM_API_KEY"))


palm_llm_config = {
    "models/text-bison-001": {
        "model": "models/text-bison-001",
    },
}


oai_llm_config = {
    "meta-llama/Llama-2-7b-chat-hf": {
        "model": "meta-llama/Llama-2-7b-chat-hf",
        "api_key": "empty",
        "api_base": "http://127.0.0.1:8000/v1",
    },
    "meta-llama/Llama-2-13b-chat-hf": {
        "model": "meta-llama/Llama-2-13b-chat-hf",
        "api_key": "empty",
        "api_base": "http://127.0.0.1:8000/v1",
    },
    "meta-llama/Llama-2-70b-chat-hf": {
        "model": "meta-llama/Llama-2-70b-chat-hf",
        "api_key": "empty",
        "api_base": "http://127.0.0.1:8000/v1",
    },
     "sambanovasystems/BLOOMChat-176B-v1": {
        "model":  "sambanovasystems/BLOOMChat-176B-v1",
        "api_key": "empty",
        "api_base": "http://127.0.0.1:8000/v1",
    },
    "gpt-3.5-turbo": {
        "model": "gpt-3.5-turbo",
        "api_key": os.environ.get("OPENAI_API_KEY"),
        "api_base": "https://api.openai.com/v1",
        "api_version": None,
    },
    "gpt-4": {
        "model": "gpt-4",
        "api_key": os.environ.get("OPENAI_API_KEY"),
        "api_base": "https://api.openai.com/v1",
        "api_version": None,
    },
}


class Completion(autogen.ChatCompletion):
    request_timeout = 300
    retry_time = 20


class ApiManager:
    model_name: str
    seed: int
    default_max_tokens: int

    def __init__(
            self,
            model_name: str,
            seed: int,
            temperature: Optional[float] = 1.0,
            default_max_tokens: Optional[int] = 945
    ):
        self.model_name = model_name
        self.seed = seed
        self.max_tokens = default_max_tokens
        self.temperature = temperature

    @property
    def api_type(self):
        return 'palm' if self.model_name in palm_llm_config.keys() else 'oai'

    def get_api_type(self):
        return self.api_type

    def palm_api(self, messages: str, choices: int = 1):

        config = {
            "max_output_tokens": self.max_tokens,
            "temperature": self.temperature,
            **messages,  # prompt
            **palm_llm_config[self.model_name]
        }
        while True:
            try:
                if choices == 1:
                    result = palm.generate_text(**config).result
                else:
                    result = [palm.generate_text(**config).result for _ in range(choices)]
            except Exception:
                print('Retrying in 20s...')
                time.sleep(20)
                continue
            break
        return result

    def oai_api(self, messages: list, choices: int = 1):
        basic_config = {
            "api_type": "open_ai",
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "seed": self.seed,  # NOTE: the dialog will be cached for the same seed
            "n": choices,
            **oai_llm_config[self.model_name]
        }

        # https://microsoft.github.io/FLAML/docs/Use-Cases/Autogen#basic-concept
        completion = Completion.create(
            messages=messages,
            **basic_config
        )
        if choices == 1:
            return completion.choices[0].message.content
        else:
            return [c.message.content for c in completion.choices]

    def __call__(self, 
                 messages: Union[list, str],
                 temperature: Optional[float] = None,
                 max_tokens: Optional[int] = None,
                 choices: Optional[int] = 1):
        if max_tokens is not None:
            self.max_tokens = max_tokens
        if temperature is not None:
            self.temperature = temperature
        if self.model_name in palm_llm_config.keys():
            resp = self.palm_api(messages, choices)
            return resp

        elif self.model_name in oai_llm_config.keys():
            resp = self.oai_api(messages, choices)
            return resp

        else:
            raise NotImplementedError


class PromptGenerator:
    """
    Generate the prompt for the given question and example.

    Args:
        api: the api manager
        sys_prompt: system prompt
        shot_type: question type, 'zero-shot' or 'few-shot'
        prompt_reinf: whether to use the prompt reinforcement (none, cot or tot)
        self_consistency: whether to use the self-consistency
        self_reflection: whether to use the self-reflection
    """

    api: ApiManager
    sys_prompt: Optional[bool]
    shot_type: Optional[str]
    prompt_reinf: Optional[str]
    return_symbol: Optional[str] = '\n'

    def __init__(
            self,
            api: ApiManager,
            system_prompt: Optional[bool] = False,
            shot_type: Optional[str] = 'zero-shot',
            prompt_reinforcement: Optional[str] = None,
    ):
        self.api = api
        self.sys_prompt = system_prompt
        self.shot_type = shot_type
        self.prompt_reinf = prompt_reinforcement

    @property
    def api_type(self):
        return self.api.get_api_type()

    def oai_prompt_generator(
            self,
            q: str,
            q_type: int,
            q_opt: Optional[List[str]] = None,
            ctx: Optional[str] = None,
            history: Optional[List[dict]] = None,
    ) -> List[dict]:
        """
        Generate the prompt for the given question and example (Open AI version).

        Args:
            args: the user arguments
            q: question content
            q_type: question type
            q_opt: question options (multiple choice only)

        Return:
            messages: the generated prompt
        """
        messages = [] if history is None else history
        prompt_reinf = f'_{self.prompt_reinf}' if self.prompt_reinf is not None else ''
        prompt_type = f'{self.shot_type}{prompt_reinf}'

        if self.sys_prompt and history is None:
            messages += [{"role": "system", "content": SYS_PROMPT_MAPPING[q_type]}]

        if ctx is not None and history is None:
            messages += [{"role": "user", "content": ctx}]

        if q_type == 0:
            q = f"{q}\n{self.return_symbol.join([f'{i}: {opt}' for i, opt in enumerate(q_opt)])}"

        if q_type == 1 and prompt_type == 'zero-shot_cot':
            cot_st1 = [{"role": "user", "content": SHORTANS_ZS_COT_ST1.format(input=q)}]
            if self.sys_prompt:
                cot_st1 = [{"role": "system", "content": SYS_PROMPT_MAPPING[q_type]}] + cot_st1
            try:
                t = self.api(cot_st1, max_tokens=128)
            except Exception as e:
                print(e)
                t = ''
            messages += [{"role": "user", "content": PROMPT_MAPPING[q_type][prompt_type].format(input=q, thought=t)}]

            return messages
        try:
            messages += [{"role": "user", "content": PROMPT_MAPPING[q_type][prompt_type].format(input=q)}]
        except Exception as e:
            print(e)

        return messages

    def palm_prompt_generator(
            self,
            q: str,
            q_type: int,
            q_opt: Optional[List[str]] = [],
            ctx: Optional[str] = None,
            history: Optional[List[dict]] = None,
    ) -> dict:
        """
        Generate the prompt for the given question and example (PaLM version).

        Args:
            args: the user arguments
            q: question content
            q_type: question type
            q_opt: question options (multiple choice only)

        Return:
            messages: the generated prompt
        """
        messages = {'prompt': ''} if history is None else history
        prompt_reinf = f'_{self.prompt_reinf}' if self.prompt_reinf is not None else ''
        prompt_type = f'{self.shot_type}{prompt_reinf}'
        sp = SYS_PROMPT_MAPPING[q_type] + self.return_symbol

        if self.sys_prompt and history is None:
            messages['prompt'] += sp

        if ctx is not None and history is None:
            messages['prompt'] += ctx + self.return_symbol

        if q_type == 0:
            q = f"{q}\n{self.return_symbol.join([f'{i}: {opt}' for i, opt in enumerate(q_opt)])}"

        if q_type == 1 and prompt_type == 'zero-shot_cot':
            cot_st1 = {'prompt': SHORTANS_ZS_COT_ST1.format(input=q)}
            if self.sys_prompt:
                cot_st1['prompt'] = sp + cot_st1['prompt']
            try:
                t = self.api(cot_st1, max_tokens=128)
            except Exception as e:
                print(e)
                t = ''
            messages['prompt'] += PROMPT_MAPPING[q_type][prompt_type].format(input=q, thought=t)

            return messages
        try:
            messages['prompt'] += PROMPT_MAPPING[q_type][prompt_type].format(input=q)
        except Exception as e:
            print(e)
        return messages

    def generate(
            self,
            q: str = "",
            q_type: int = 0,
            q_opt: Optional[List[str]] = None,
            ctx: Optional[str] = None,
            history: Optional[List[dict]] = None,
    ):
        if self.api_type == 'oai':
            messages = self.oai_prompt_generator(q, q_type, q_opt, ctx, history)
        else:
            messages = self.palm_prompt_generator(q, q_type, q_opt, ctx, history)

        return messages
