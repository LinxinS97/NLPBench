# NLPBench: Evaluating NLP-Related Problem-solving Ability in Large Language Models


NLPBench is a novel benchmark for Natural Language Processing problems consisting of 378 questions sourced from the NLP course final exams at Yale University. 

## Data
Our example questions:
![Example Questions](assets/q_eg.png)
**Our dataset is licensed under the [CC BY-ND](https://creativecommons.org/licenses/by-nd/4.0/deed.en)**. You can download our dataset through [this link](https://drive.google.com/drive/folders/1haGLwzdZ_fejN7s-nBpDlz8gZPowZSZN?usp=sharing).

## Environment Preparation
You can import our environment from the `environment.yml` by
```bash
conda env create -f environment.yml
```
then activate our conda environment by
```bash
conda activate NLPBench
```

## Evaluation
Our evaluations are based on both online (GPT-3.5, GPT-4, and PaLM 2) and open-sourced (LLAMA 2, Falcon, Bloom, etc.) LLMs.

### For Online LLM
Online LLM often requires an `API-key` before access. If you want to access the OpenAI model, you need to add the `OPENAI_API_KEY` to the system environment as follows:
```bash
export OPENAI_API_KEY="YOUR OPENAI API KEY"
```
and for PaLM 2, you need to add the `PALM_API_KEY` to your system environment as follows:
```bash
export PALM_API_KEY="YOUR PALM API"
```

### For Open-sourced LLM
We use [vLLM](https://github.com/vllm-project/vllm) to start an openai-like endpoint for evaluation. All configurations are summarized in `./utils/utils.py:oai_llm_config`. Check [this list](https://vllm.readthedocs.io/en/latest/models/supported_models.html) for information on the supported open-source model. 

Basically, if you want to evaluate other open-sourced models, add your model's configuration in the following format into the `oai_llm_config`:
```json
"HUGGINGFACE REPO": {
    "model": "HUGGINGFACE REPO",
    "api_key": "empty",
    "api_base": "YOUR ENDPOINT HOST, DEFAULT: http://127.0.0.1:8000/v1",
}
```
then start the endpoint with the following script:
```bash
bash scripts/serving.sh [-m HUGGINGFACE REPO][-n NUMBER OF GPUs][-a HOST ADDRESS, DEFAULT: 127.0.0.1][-p PORT, DEFAULT: 8000]
```

### Run Evaluation
We have two steps for evaluation: (1) solving the problems and (2) calculating the accuracy.
We adopt [sacred](https://github.com/IDSIA/sacred) to manage our configurations. All configs can be found in `./configs`. You can also add your config by creating a specific `yaml` file. As an example, you can run the following code to let `GPT-3.5` with only `zero-shot` prompting answer the questions without context:
```bash
python run.py with configs/zero-shot.yaml model_name='gpt-3.5-turbo' ctx=False
```
The answer results will be saved in `./res/{SEED}/no_ctx/zero-shot_gpt-3.5-turbo.json`.
You can evaluate the above result by running the following code:
```
python evaluate.py
```
Then the result will be saved in `./res/{SEED}/`

## Prompt
All the prompts in our evaluation can be found in `./prompts`, including prompt for question answering (`qa_prompt.py`), system prompt (`sys_prompt.py`), and prompt for tree-of-thought (`tot_prompt.py`). You can customize your prompt by modifying the above three files.

## Citation
If you think our repository and result is useful, please cite our paper by
```
@misc{song2023nlpbench,
      title={NLPBench: Evaluating Large Language Models on Solving NLP Problems}, 
      author={Linxin Song and Jieyu Zhang and Lechao Cheng and Pengyuan Zhou and Tianyi Zhou and Irene Li},
      year={2023},
      eprint={2309.15630},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```