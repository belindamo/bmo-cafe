import os

from anthropic import Anthropic

from utils.config import ModelResponse
from utils.helpers import get_numerical_answer

def claude(
    model_name: str, question: str, system_prompt: str = None) -> ModelResponse:
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model=model_name,
        max_tokens=1000,
        temperature=0,
        system=system_prompt if system_prompt is not None else '',
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question,
                    }
                ],
            }
        ],
    )
    return ModelResponse(
        model=model_name,
        question=question,
        answer=str(message.content[0].text),
        numerical_answer= get_numerical_answer(message.content[0].text),
        prompt=system_prompt if system_prompt else None,
    )
