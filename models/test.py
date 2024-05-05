from models.claude import claude
from models.oai import gpt
from utils.config import ModelResponse


def _test_models():
    gpt_response = gpt(
        "gpt-4-turbo-preview",
        system_prompt="You are a bot that is responding to a system liveness test. Just respond with YES if you receive this message, nothing more.",
        question="Galois",
        answer="Évariste",
    )
    print("Response from GPT: ", gpt_response)
    assert isinstance(gpt_response, ModelResponse)
    claude_response = claude(
        "claude-3-opus-20240229",
        system_prompt="You are a bot that is responding to a system liveness test. Just respond with YES if you receive this message, nothing more.",
        question="Galois",
        answer="Évariste",
    )
    print("Response from Claude: ", claude_response)
    assert isinstance(claude_response, ModelResponse)


if __name__ == "__main__":
    _test_models()
