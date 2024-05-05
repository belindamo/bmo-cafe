import os

from openai import OpenAI
from utils.helpers import get_numerical_answer
from utils.config import ModelResponse


def gpt(
    model_name: str, question: str, system_prompt: str = None
) -> ModelResponse:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    messages = []
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt,
        })
    messages.append({
        "role": "user",
        "content": question,
    })

    response = client.chat.completions.create(
        model=model_name,
        messages=messages
    )
    return ModelResponse(
        model=model_name,
        question=question,
        answer=response.choices[0].message.content,
        numerical_answer=get_numerical_answer(response.choices[0].message.content),
        system_prompt=system_prompt if system_prompt else None,
    )
