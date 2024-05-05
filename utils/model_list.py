import os

from typing import List
from utils.config import ModelName

openai_models = [
    "gpt-3.5-turbo-0125",
    "gpt-4-0613",
    os.environ.get("OPENAI_FINETUNING_ID_3.5_100"),
    os.environ.get("OPENAI_FINETUNING_ID_3.5_1000"),
    os.environ.get("OPENAI_FINETUNING_ID_3.5_7473")
]  # https://platform.openai.com/docs/models
anthropic_models = [
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
]  # https://docs.anthropic.com/claude/docs/models-overview


def list_available_models() -> dict[str, List[str]]:
    """
    Lists all available OpenAI and Anthropic models.

    :return: A list of model names.
    """
    return {"openai": openai_models, "anthropic": anthropic_models}


def is_model_available(model_name: ModelName) -> bool:
    """
    Checks if the given model name is in the list of available models.

    :param model_name: The name of the model to check.
    :return: True if the model is available, False otherwise.
    """
    if model_name.provider.lower() == "openai":
        return model_name.model_name in openai_models
    elif model_name.provider.lower() == "anthropic":
        return model_name.model_name in anthropic_models
    else:
        return False
