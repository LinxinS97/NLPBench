# NLPBench: Evaluating NLP-Related Problem-solving Ability in Large Language Models


NLPBench is a novel benchmark for Natural Language Processing problems consisting of 378 questions scourced from some universities' final exam. 

## Data
Our example questions:
![Example Questions](assets/q_eg.png)
You need to agree a license before requesting the dataset, the download link will be opened soon.

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
Our evaluation are based on both online (GPT-3.5, GPT-4 and PaLM 2) and open sourced (LLAMA 2, Falcon, Bloom, etc.) LLMs.

### For Online LLM
Online LLM often require a `API-key` before access. If you want to access the OpenAI model, you need to add the `OPENAI_API_KEY` to the system environment as follows:
```bash
export OPENAI_API_KEY="YOUR OPENAI API KEY"
```
and for PaLM 2, you need to add the `PALM_API_KEY` to your system environment as follows:
```bash
export PALM_API_KEY="YOUR PALM API"
```

### For Open-sourced LLM
We use [vLLM](https://github.com/vllm-project/vllm) to start an openai-like endpoint for evaluation. All configurations are summarized in `./utils/utils.py:oai_llm_config`. Check [this list](https://vllm.readthedocs.io/en/latest/models/supported_models.html) for the information of supported opensourced model. 

Basically, if you want to evaluate other opensourced models, add your model's configuration in the following format into the `oai_llm_config`:
```json
"HUGGINGFACE REPO": {
    "model": "HUGGINGFACE REPO",
    "api_key": "empty",
    "api_base": "YOUR ENDPOINT HOST, DEFAULT: http://127.0.0.1:8000/v1",
}
```
then start the endpoint by the following script:
```bash
bash scripts/serving.sh [-m HUGGINGFACE REPO][-n NUMBER OF GPUs][-a HOST ADDRESS, DEFAULT: 127.0.0.1][-p PORT, DEFAULT: 8000]
```

### Run Evaluation
We have two steps for evaluation: (1) solving the problems and (2) calculate the accuracy.
We adopt [sacred](https://github.com/IDSIA/sacred) to manage our configurations. All configs can be found in `./configs`, you can also add your config by creating a specific `yaml` file. As an example, you can run the following code to let `GPT-3.5` with only `zero-shot` prompting answer the questions without context:
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
All the prompt in our evaluation can be found in `./prompts`, including prompt for question answering (`qa_prompt.py`), system prompt (`sys_prompt.py`), and prompt for tree-of-thought (`tot_prompt.py`). You can customize your prompt by modifying the above three files.

