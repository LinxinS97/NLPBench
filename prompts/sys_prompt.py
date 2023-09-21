SYS_PROMPT_MULTICHOICE = """Answer the multiple choice questions in the field of Natural Language Processing (NLP).
You should select a single (or a couple of) answer(s) from the given options. 
"""

SYS_PROMPT_SHORTANS = """Answer the short answer questions in the field of Natural Language Processing (NLP).
You should provide a concise short answer for the question.
All the math symbols in your answer must be converted to LaTeX format (e.g., \\pi, \\sqrt{{2}}). 
"""

SYS_PROMPT_MATH = """Answer the mathematics questions in the field of Natural Language Processing (NLP).
You should provide a (or a couple of) number(s) or LaTeX expression(s). 
When the answer is a fraction, please use \\frac{{}}{{}} to express it (e.g., \\frac{{1}}{{2}}).
When the answer is a vector or matrix, please use \\begin{{bmatrix}} \\end{{bmatrix}} to express it (e.g., \\begin{{bmatrix}} 1 & 2 \\\\ 3 & 4 \\end{{bmatrix}}).
You should not trun \\pi, \\sqrt{{2}}... to a decimals, but use the original format.
"""

SYS_PROMPT_MAPPING = {
    0: SYS_PROMPT_MULTICHOICE,
    1: SYS_PROMPT_SHORTANS,
    2: SYS_PROMPT_MATH
}
