# bmo.cafe

## Getting started

Bmo Cafe helps you generate and schedule recurring task scripts using LLMs. Basically, anything that can be thrown in a single Python file can be automated. The two task types that are currently implemented are:

- Generate browser requests based on a text prompt
- Generate and run Python functions and tests based on a text prompt

Clone or fork this repository. Make sure [poetry is installed](https://python-poetry.org/docs/). 

If you don't already have your OpenAI key set up, [follow the instructions on their site](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key).

Then, run:
- `poetry install`
- `poetry run python main.py`

Be sure to run your scripts from the root directory since some files rely on absolute file paths.

Finally, add `my_data.yaml` with your data. For example, to run the check for SF parking tickets, add the following information: 
```
car_license: 'YOUR_LICENSE_PLATE_NUMBER'
car_state: 'YOUR_LICENSE_PLATE_STATE'
```

And you're all set up! ☕️ 

## What tasks can this cafe do?

You can check out the example tasks in the `tasks` folder. You can do things like:
- Do things in the web browser that are based on HTTPS requests and responses
- Write in your style of voice

## 2 Paths
There are two ways you can create a task:
1. You provide the Python script that is executed.
2. A model automatically generates the Python script. (Sadly this only works at the moment for Python function generation with 1 number input and 1 number output. It does generate test sets though, which is cool.)

A task is represented as a single folder <TASK_NAME>. In this folder, you will find:
- `index.py`: this is the script that is executed.
- `streams/`: this is where the output streams of task execution is stored. It should be generated upon running the task for the first time.
- `config.yaml`: this is where the task configuration is stored.
- `tests.csv` (Optional): if this exists, it contains the input/output pairs to ensure that index.py does what it is supposed to.

Create a task by running `poetry run python main.py` and following the prompts. Add your script afterwards, if you are adding your own. Be sure to follow the steps below first. 

## Future implementations

Some future tasks:
- Generate text based on some writing sample
- Generate text edits based on some writing sample
- Generate natural language checks to ensure your text is faithful to writing sample