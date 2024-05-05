import json
from openai import OpenAI
import os

def get_numerical_answer(model_answer: str) -> int:
    '''
    This function is used to extract a numerical answer from a given question and answer.
    It uses a gpt-4-0613 model to parse the answer and return a numerical value.
    '''

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    gpt_response = client.chat.completions.create(
        model="gpt-4-0613",
        messages=[
            {
                "role": "user",
                "content": f"Please parse a single number out of answer. Respond only with a number. \n model_answer: {model_answer}"
            }
        ],
    )
    response = gpt_response.choices[0].message.content

    # Extract the numerical answer from the gpt response
    if response.isdigit():
        numerical_answer = int(response)
    else:
        numerical_answer = None
    return numerical_answer


def extract_data_from_gsm8k(file_path="../datasets/GSM8K/test.jsonl") -> list[dict]:
    '''
    Each dictionary in the list represents a single entry from the GSM8K dataset.
    Each dictionary contains three keys:
    'question': The question from the dataset entry.
    'answer': The answer from the dataset entry.
    'numerical_answer': The numerical value extracted from the answer.
    '''

    data = []
    with open(file_path, "r") as file:
        for line in file:
            entry = json.loads(line)
            question = entry.get("question", "")
            answer = entry.get("answer", "")
            final_answer = answer.split("#### ")[-1] if "#### " in answer else answer
            if final_answer.isdigit():
                numerical_answer = int(final_answer)
            else:
                raise ValueError("The final answer is not a digit.")
            
            data.append(
                {
                    "question": question,
                    "answer": answer,
                    "numerical_answer": numerical_answer
                }
            )
    return data


def main():
    data = extract_data_from_gsm8k()
    if data:
        print(data[13])
    else:
        print("No data found.")


if __name__ == "__main__":
    main()
