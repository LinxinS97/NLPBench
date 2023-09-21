MULTICHOICE_STD_ZS = '''
Answer the final multiple choice question. 
Your output must be only numbers spliting by comma (e.g., 0,1,...) with no descriptions.

Example Input:
ChatGPT is created by which of the following companies?
0: Google
1: Meta
2: Microsoft
4: Amazon
3: OpenAI

Example Output:
3

Example Input:
This is the input question, choose the correct answer.
0: Correct answer
1: Option 2
2: Correct answer
3: Option 4

Example Output:
0,2

Example Input:
GPT-4 is created by OpenAI.
0: True
1: False

Example Output:
0

Input (You need to answer this question): 
{input}

Output: 
'''


MULTICHOICE_STD_ZS_COT = '''
Answer the final multiple choice question. Your output must be only numbers spliting by comma (e.g., 0,1,...) with no descriptions.

Example Input:
ChatGPT is created by which of the following companies?
0: Google
1: Meta
2: Microsoft
4: Amazon
3: OpenAI

Example Thought:
ChatGPT is a large-scale transformer-based language model, created by OpenAI at 2022.

Example Output:
3

Example Input:
This is the input question, choose the correct answer.
0: Correct answer
1: Option 2
2: Correct answer
3: Option 4

Example Thought:
This is a multiple choice question, the "correct answer" appears at index 0 and 2.

Example Output:
0,2

Example Input:
GPT-4 is created by OpenAI.
0: True
1: False

Example Thought:
GPT-4 is created by OpenAI at 2022.

Example Output:
0

Input (You need to answer this question): 
{input}

Output: 
'''


MULTICHOICE_STD_FS = '''
Answer the final multiple choice question. Your output must be only numbers spliting by comma (e.g., 0,1,...) with no descriptions.

Example Input:
What is the main challenge(s) of NLP?
0: Handling Ambiguity of Sentences
1: Handling Tokenization
2: Handling POS-Tagging
3: All of the mentioned

Example Output:
0

Example Input:
What is the field of Natural Language Processing (NLP)>
0: Computer Science
1: Artificial Intelligence
2: Linguistics
3: All of the mentioned

Example Output:
3

Example Input:
Choose from the following areas where NLP can be useful.
0: Automatic Text Summarization
1: Automatic Question-Answering Systems
2: Information Retrieval
3: All of the mentioned

Example Output:
3

Input (You need to answer this question): 
{input}

Output: 
'''


MULTICHOICE_STD_FS_COT = '''
Answer the final multiple choice question. Your output must be only numbers spliting by comma (e.g., 0,1,...) with no descriptions.

Example Input:
What is the main challenge(s) of NLP?
0: Handling Ambiguity of Sentences
1: Handling Tokenization
2: Handling POS-Tagging
3: All of the mentioned

Example Thought:
There are enormous ambiguity exists when processing natural language.

Example Output:
0

Example Input:
What is Machine Translation?
0: Converts one human language to another
1: Converts human language to machine language
2: Converts any human language to English
3: Converts Machine language to human language

Example Thought:
The best known example of machine translation is google translator, which help people to translate one language to another.

Example Output:
0

Example Input:
What is Coreference Resolution?
0: Anaphora Resolution
1: Given a sentence or larger chunk of text, determine which words (“mentions”) refer to the same objects (“entities”)
2: All of the mentioned
3: None of the mentioned

Example Thought:
Anaphora resolution is a specific type of coreference resolution.

Example Output:
1

Input (You need to answer this question): 
{input}

Output: 
'''


SHORTANS_ZS = '''
Answer the following short answer question. Your answer should be no more then 150 words.

Input (You need to answer this question): 
{input}

Output: 
'''


SHORTANS_ZS_COT_ST1 = '''
Answer the following short answer question. Your answer should be no more then 150 words.

Input (You need to answer this question): 
{input}

Let's think step by step! Output your thought of the question first:
'''


SHORTANS_ZS_COT = '''
Answer the following short answer question. Your answer should be no more then 150 words.

Input (You need to answer this question): 
{input}

Your thought:
{thought}

Output: 
'''


SHORTANS_FS = '''
Answer the following short answer question. Your answer should be no more then 150 words.

Example Input:
Order the following syntactic features in decreasing order by salience (according to the Lappin/Leass algorithm for anaphora resolution): direct object (accusative), indirect object, subject, recency.

Example Output:
From strongest to weakest:
1. Recency
2. Subject
3. Direct object
4. Indirect object

Example Input: 
List any two real-life applications of Natural Language Processing.

Example Output:
1. Google Translate.
2. ChatGPT.

Example Input:
What are stop words?

Example Output:
Stop words are said to be useless data for a search engine. Words such as articles, prepositions, etc. are considered stop words. 
There are stop words such as was, were, is, am, the, a, an, how, why, and many more.

Input (You need to answer this question): 
{input}

Output: 
'''


SHORTANS_FS_COT = '''
Answer the following short answer question. Your answer should be no more then 150 words.

Example Input:
Order the following syntactic features in decreasing order by salience (according to the Lappin/Leass algorithm for anaphora resolution): direct object (accusative), indirect object, subject, recency.

Example Thought:
The following is the order of the given syntactic features in decreasing order by salience (according to the Lappin/Leass algorithm for anaphora resolution):
Direct object (accusative): The least salient antecedent is the direct object of the sentence.
Indirect object: The third most salient antecedent is the indirect object of the sentence.
Subject: The next most salient antecedent is the subject of the sentence.
Recency: The most salient antecedent is the noun phrase that occurs most recently in the discourse.

Example Output:
From strongest to weakest:
1. Recency
2. Subject
3. Direct object
4. Indirect object

Example Input: 
List any two real-life applications of Natural Language Processing.

Example Thought:
Natural Language Processing (NLP) has a wide range of applications across various industries due to its ability to understand and generate human language.
There are a lot of applications of NLP in deep translation (like google translate), chatbot (like ChatGPT) and many more.

Example Output:
1. Google Translate.
2. ChatGPT.

Example Input:
What are stop words?

Example Thought:
Stop words are said to be useless data for a search engine. 
There are stop words such as was, were, is, am, the, a, an, how, why, and many more.

Example Output:
Words such as articles, prepositions, etc. are considered stop words. 

Input (You need to answer this question): 
{input}
'''


MATH_ZS = '''
Answer the following math question. Your answer should be a number, a list of numbers, or a LaTeX expression.

Example Input:
1 + 1

Example Output:
2

Example Input:
$\\frac{{1}}{{2}} + \\frac{{1}}{{3}}$

Example Output:
\\frac{{5}}{{6}}

Example Input:
$f(x) = 4x^2 + 3y$
Solve the $\\frac{{\\partial f(x)}}{{\\partial x}}$

Example Output:
8x

Input (You need to answer this question):
{input}

Output:
'''


MATH_ZS_COT = '''
Answer the following math question. Your answer should be a number, a list of numbers, or a LaTeX expression.

Example Input:
1 + 1

Example Thought:
1 + 1 = 2

Example Output:
2

Example Input:
$\\frac{{1}}{{2}} + \\frac{{1}}{{3}}$

Example Thought:
$\\frac{{1}}{{2}} + \\frac{{1}}{{3}} = \\frac{{5}}{{6}}$

Example Output:
\\frac{{5}}{{6}}

Example Input:
$f(x) = 4x^2 + 3y$
Solve the $\\frac{{\\partial f(x)}}{{\\partial x}}$

Example Thought:
$\\frac{{\\partial f(x)}}{{\\partial x}} = 2\\times 4x + 0$

Example Output:
8x

Example Input (You need to answer this question):
{input}

Output:
'''


MATH_FS = '''
Answer the following math question. Your answer should be a number, a list of numbers, or a LaTeX expression.

Example Input:
$\\frac{{1}}{{2}} + \\frac{{1}}{{3}}$

Example Output:
\\frac{{5}}{{6}}

Example Input:
$f(x) = 4x^2 + 3y$
Solve the $\\frac{{\\partial f(x)}}{{\\partial x}}$

Example Output:
8x

Example Input:
Consider the following bilingual (Spanish-English) corpus.
gato blanco
white cat

el gato
the cat

Considering only the following three alignment types:
1. || {{1,2}}
2. X {{2,1}}

Start with a uniform distribution for $t(white|gato)$, $t(white|blanco)$, $t(cat|gato)$, $t(cat|blanco)$, $t(cat|el)$, $t(the|el)$, and $t(the|gato)$. 
Show the values of them after two iterations of the EM algorithm.

Example Output:
\\frac{{1}}{{6}},\\frac{{2}}{{3}},\\frac{{2}}{{3}},\\frac{{1}}{{3}},\\frac{{1}}{{3}},\\frac{{2}}{{3}},\\frac{{1}}{{6}}

Input:
{input}

Output (You need to answer this question):
'''


MATH_FS_COT = '''
Answer the following math question. Your answer should be a number, a list of numbers, or a LaTeX expression.

Example Input:
$\\frac{{1}}{{2}} + \\frac{{1}}{{3}}$

Example Thought:
1 + 1 = 2

Example Output:
\\frac{{5}}{{6}}

Example Input:
$f(x) = 4x^2 + 3y$
Solve the $\\frac{{\\partial f(x)}}{{\\partial x}}$

Example Thought:
$\\frac{{\\partial f(x)}}{{\\partial x}} = 2\\times 4x + 0$

Example Output:
8x

Example Input:
Consider the following bilingual (Spanish-English) corpus.
gato blanco
white cat

el gato
the cat

Considering only the following three alignment types:
1. || {{1,2}}
2. X {{2,1}}

Start with a uniform distribution for $t(white|gato)$, $t(white|blanco)$, $t(cat|gato)$, $t(cat|blanco)$, $t(cat|el)$, $t(the|el)$, and $t(the|gato)$. 
Show the values of them after two iterations of the EM algorithm.

Example Thought:
Initialization:
$t(white|gato)=\\frac{{1}}{{2}}$
$t(white|blanco)=\\frac{{1}}{{2}}$
$t(cat|gato)=\\frac{{1}}{{3}}$
$t(cat|blanco)=\\frac{{1}}{{3}}$
$t(cat|el)=\\frac{{1}}{{3}}$
$t(the|el)=\\frac{{1}}{{2}}$
$t(the|gato)=\\frac{{1}}{{2}}$

$\\textbf{{First Iteration:}}$

gato blanco
white cat

For alignment type X:
$p(a,f|e)=\\frac{{1}}{{2}}\\times \\frac{{1}}{{3}}=\\frac{{1}}{{6}}$
$p(a|e,f)=\\frac{{1}}{{2}}$

For alignment type ||:
$p(a, f|e) = \\frac{{1}}{{2}}\\times\\frac{{1}}{{3}} = \\frac{{1}}{{6}}$
$p(a|e, f) = \\frac{{1}}{{2}}$

el gato
the cat

For alignment type X:
$p(a,f|e)=\\frac{{1}}{{2}}\\times \\frac{{1}}{{3}}=\\frac{{1}}{{6}}$
$p(a|e,f)=\\frac{{1}}{{2}}$

For alignment type ||:
$p(a, f|e) = \\frac{{1}}{{2}}\\times\\frac{{1}}{{3}} = \\frac{{1}}{{6}}$
$p(a|e, f) = \\frac{{1}}{{2}}$

Fractional Counts:
$t(white|gato)=\\frac{{1}}{{2}}$
$t(white|blanco)=\\frac{{1}}{{2}}$
$t(cat|gato)=\\frac{{1}}{{2}}+\\frac{{1}}{{2}}=1$
$t(cat|blanco)=\\frac{{1}}{{2}}$
$t(cat|el)=\\frac{{1}}{{2}}$
$t(the|el)=\\frac{{1}}{{2}}$
$t(the|gato)=\\frac{{1}}{{2}}$

Normalize to get updated parameters:
$t(white|gato)=\\frac{{1}}{{4}}$
$t(white|blanco)=\\frac{{1}}{{2}}$
$t(cat|gato)=\\frac{{1}}{{2}}$
$t(cat|blanco)=\\frac{{1}}{{2}}$
$t(cat|el)=\\frac{{1}}{{2}}$
$t(the|el)=\\frac{{1}}{{2}}$
$t(the|gato)=\\frac{{1}}{{4}}$

$\\textbf{{Second Iteration:}}$
gato blanco\nwhite cat

For alignment type X:
$p(a,f|e)=\\frac{{1}}{{2}}\\times \\frac{{1}}{{2}}=\\frac{{1}}{{4}}$
$p(a|e,f)=\\frac{{2}}{{3}}$

For alignment type ||:
$p(a, f|e) = \\frac{{1}}{{4}}\\times\\frac{{1}}{{2}} = \\frac{{1}}{{8}}$
$p(a|e, f) = \\frac{{1}}{{3}}$

el gato
the cat

For alignment type X:
$p(a,f|e)=\\frac{{1}}{{4}}\\times \\frac{{1}}{{2}}=\\frac{{1}}{{8}}$
$p(a|e,f)=\\frac{{1}}{{3}}$

For alignment type ||:
$p(a, f|e) = \\frac{{1}}{{2}}\\times\\frac{{1}}{{2}} = \\frac{{1}}{{4}}$
$p(a|e, f) = \\frac{{2}}{{3}}$

Fractional Counts:
$t(white|gato)=\\frac{{1}}{{3}}$
$t(white|blanco)=\\frac{{2}}{{3}}$
$t(cat|gato)=\\frac{{2}}{{3}}+\\frac{{2}}{{3}}=\\frac{{4}}{{3}}$
$t(cat|blanco)=\\frac{{1}}{{3}}$
$t(cat|el)=\\frac{{1}}{{3}}$
$t(the|el)=\\frac{{2}}{{3}}$
$t(the|gato)=\\frac{{1}}{{3}}$

Finally, you can normalize to get updated parameters.

Example Output:
\\frac{{1}}{{6}},\\frac{{2}}{{3}},\\frac{{2}}{{3}},\\frac{{1}}{{3}},\\frac{{1}}{{3}},\\frac{{2}}{{3}},\\frac{{1}}{{6}}

Input (You need to answer this question):
{input}

Output:
'''


CTX = '''The context of the following questions is:
{context}
'''

PROMPT_MAPPING = {
    0: {
        'zero-shot': MULTICHOICE_STD_ZS,
        'few-shot': MULTICHOICE_STD_FS,
        'zero-shot_cot': MULTICHOICE_STD_ZS_COT,
        'few-shot_cot': MULTICHOICE_STD_FS_COT,
        'zero-shot_tot': MULTICHOICE_STD_ZS_COT,
        'few-shot_tot': MULTICHOICE_STD_FS_COT
    },
    1: {
        'zero-shot': SHORTANS_ZS,
        'few-shot': SHORTANS_FS,
        'zero-shot_cot': SHORTANS_ZS_COT,
        'few-shot_cot': SHORTANS_FS_COT,
        'zero-shot_tot': SHORTANS_ZS_COT,
        'few-shot_tot': SHORTANS_FS_COT
    },
    2: {
        'zero-shot': MATH_ZS,
        'few-shot': MATH_FS,
        'zero-shot_cot': MATH_ZS_COT,
        'few-shot_cot': MATH_FS_COT,
        'zero-shot_tot': MATH_ZS_COT,
        'few-shot_tot': MATH_FS_COT
    }
}
