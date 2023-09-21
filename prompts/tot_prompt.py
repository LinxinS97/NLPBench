SOLUTION_PROMPT = """You're an Tree-of-Thoughts, an superintelligent AI model devoted to help Human by any means necessary. 
Your purpose is to generate a series of solutions to comply with the user's instructions, you must generate solutions on the basis of determining the most reliable solution in the shortest amount of time, while taking rejected solutions into account and learning from them. 
Considering the reasoning provided:\n\n
###'{state_text}'\n\n###
Devise the best possible solution for the task: {initial_prompt}, Here are evaluated solutions that were rejected: 
###{rejected_solutions}###, 
complete the {initial_prompt} without making the same mistakes you did with the evaluated rejected solutions. 
Be simple. Be direct. Provide intuitive solutions as soon as you think of them."""

STATE_PROMPT = """Given a question: 
'{initial_prompt}', value the following past solutions as a float number between 0 and 1.\n
If the past solution is not directly and concretely in achieving the goal, give it a low score.
Past solutions:\n\n
'{state_text}'
"""

VOTE_PROMPT = """Given the following states of reasoning, vote for the best state utilizing an scalar value 1-10:\n{states_text}\n\nVote, on the probability of this state of reasoning achieveing {initial_prompt} and become very pessimistic very NOTHING ELSE"""