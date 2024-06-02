import os

from openai import OpenAI
from pydantic import BaseModel
from typing import Optional

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def gpt(
    model: str, question: str = None, messages = [], system_prompt: str = None
) -> str:
    if question is not None:
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
        model=model,
        messages=messages
    )
    return response.choices[0].message.content
