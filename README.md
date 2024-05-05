# bmo.cafe

## What does this cafe do?

Bmo Cafe helps you be super productive, like a shot of coffee. We help:

- Generate Python code based on a text prompt
- Generate HTTPS requests based on a text prompt
- Generate natural language or Python checks to ensure Python code works
- Generate text based on some writing sample
- Generate text edits based on some writing sample
- Generate natural language checks to ensure your text is faithful to writing sample

Uniquely, our cafe also generate tests with examples so that you can check whether the generation was good.

You can check out the example tasks in the `tasks` folder. You can do things like:
- International Math Olympiad problems
- Browser tasks that are based on HTTPS requests and responses
- Writing in your style of voice

## Getting started

Clone or fork this repository. Make sure [poetry is installed](https://python-poetry.org/docs/). 

If you don't already have your OpenAI key set up, [follow the instructions on their site](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key).


Finally, run:
- `poetry install`
- `poetry run python main.py`

Be sure to run your scripts from the root directory since some files rely on absolute file paths.

And you're all set up! ☕️ 
