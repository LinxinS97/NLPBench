from solve import Solver
from sacred import Experiment

ex = Experiment("LLM")


@ex.config
def config():
    model_name = 'gpt-3.5-turbo'
    config = 'zero-shot'
    ctx = False


@ex.automain
def run(
        model_name,
        seed,
        shot_type,
        prompt_r,
        sys,
        ctx,
        max_tokens,
        self_consistency,
        self_reflection
):
    if ctx:
        data_path = "data/w_ctx.json"
    else:
        data_path = "data/wo_ctx.json"

    solver = Solver(
        data_path=data_path,
        model_name=model_name,
        seed=seed,
        shot_type=shot_type,
        prompt_r=prompt_r,
        sys=sys,
        ctx=ctx,
        max_tokens=max_tokens,
        self_consistency=self_consistency,
        self_reflection=self_reflection,
    )

    solver.run()
