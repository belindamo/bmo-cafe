import os
from openai import OpenAI

client = OpenAI()

def solve_imo_problem(problem: str):
  system_prompt = """You are a gold medalist in International Math Olympiad. 

  You are tasked to answer International Math Olympiad questions. The correct answers to all questions can only be 'yes', 'no', or a single numeric answer.
  Please show your step-by-step reasoning and calculations before providing the final answer.
  
  Final answer of 'yes', 'no' or numeric answer should be at the end between <answer> and </answer>"""
  
  response = client.chat.completions.create(
    model='gpt-4-0613',
    messages=[
      { 'role': 'system', 'content': system_prompt},
      { 'role': 'user', 'content': problem }
    ]
  )

  text = response.choices[0].message.content.strip()
  print('Reasoning: ', text)
  start_index = text.find('<answer>')
  end_index = text.find('</answer>')
  final_answer = text
  if start_index != -1 and end_index != -1:
    text = text[start_index + len('<answer>'):end_index].strip()
  return text

if __name__ == "__main__":
  problem = """A4. Let $a_{{0}}, a_{{1}}, a_{{2}}, \ldots$ be a sequence of real numbers such that $a_{{0}}=0, a_{{1}}=1$, and for every $n \geqslant 2$ there exists $1 \leqslant k \leqslant n$ satisfying

  $$
  a_{{n}}=\frac{a_{{n-1}}+\cdots+a_{{n-k}}}{k}
  $$

  Find the maximal possible value of $a_{{2018}}-a_{{2017}}$."""
  actual_answer = "$\frac{{2016}}{{2017^{{2}}}}$"
  answer = solve_imo_problem(problem)
  print('Problem: ', problem)
  print('Actual answer: ', actual_answer)
  print('AI answer: ', answer)
  
