from typing import List, Optional
from pydantic import BaseModel

SYSTEM_PROMPT = """<DESCRIPTION> You are post-graduate mathematics student at MIT working on the side to answer and grade some math questions. This is a preliminary test to see how you do! Answer to the best of your ability. </DESCRIPTION>
<HOW_TO_RESPOND> Respond with a SINGULAR number, the answer to the computation question. For example, respond with only: "53", "0", "-1203923" </HOW_TO_RESPOND>
"""

class ModelResponse(BaseModel):
    model: str
    answer: str
    numerical_answer: int | None # This answer is extracted with an additional call
    system_prompt: Optional[str]

class AggregateModelResponse(BaseModel):
    name: str
    description: str
    model_responses: List[ModelResponse]


class ModelName(BaseModel):
    provider: str
    model_name: str
