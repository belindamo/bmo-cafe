import importlib
import os
import asyncio
import csv
import yaml
from openai import OpenAI
from datetime import datetime
from schedule_task import schedule_task, check_scheduled_task
from update_lexicon import update_lexicon
from generate_task import generate_task

client = OpenAI()

COMMANDS = """
- l: list all tasks
- g: generate a new task
- r <task_name>: run an existing task
- t <task_name>: run test for an existing task
- s <task_name> <"daily" or every number of seconds>: schedule a task
- a: see all scheduled tasks
- q: quit
- or just chat with me ☕️"""

OPENAI_TOKEN_COST = {
    'gpt-4': {
        'input': 30 / 1000000,
        'output': 60 / 1000000
    },
    'gpt-4-32k': {
        'input': 60 / 1000000,
        'output': 120 / 1000000
    },
    'gpt-3.5-turbo-0125': {
        'input': 0.5 / 1000000,
        'output': 1.5 / 1000000
    },
    'gpt-3.5-turbo-instruct': {
        'input': 1.5 / 1000000,
        'output': 2 / 1000000
    },
}

last_request_usage = {
    'input_cost': 0,
    'output_cost': 0,
    'input': 0,
    'output': 0,
}
total_usage = {
    'input_cost': 0,
    'output_cost': 0,
    'input': 0,
    'output': 0,
}

# --- Helpers ---

# This is abstracted out in order to track number of tokens.
def openai_request(*args, **kwargs):
    response = client.chat.completions.create(*args, **kwargs)

    # Get the token usage information from the API response
    token_usage = response.usage
    
    # Update token usage
    last_request_usage['input'] = token_usage.prompt_tokens
    last_request_usage['output'] = token_usage.completion_tokens
    last_request_usage['input_cost'] = token_usage.prompt_tokens * OPENAI_TOKEN_COST[kwargs['model']]['input'] 
    last_request_usage['output_cost'] = token_usage.completion_tokens * OPENAI_TOKEN_COST[kwargs['model']]['output']
    total_usage['input'] += last_request_usage['input']
    total_usage['output'] += last_request_usage['output']
    total_usage['input_cost'] += last_request_usage['input_cost']
    total_usage['output_cost'] += last_request_usage['output_cost']

    return response


# --- Kiks ---

class Kik:
    def __init__(self, folder_path):
        self.name = folder_path
        with open(f"{folder_path}/index.yaml", 'r') as file:
            data = yaml.safe_load(file)
        self.description = data['description']
        self.model = data['model']
        self.actions = data['actions']
        self.values = data['values']
        self.references = data['references'] if 'references' in data else None
        self.additional_api_data = data['additional_api_data'] if 'additional_api_data' in data else None

        self.messages = [{'role': 'system', 'content': self._system_prompt()}]
        self.current_session = []
        
    
    def _system_prompt(self):
        if not hasattr(self, 'description') or not hasattr(self, 'actions') or not hasattr(self, 'values'):
            raise AttributeError("Required attributes 'description', 'actions', or 'values' not defined for Kik.")
        
        return f"""
        {self.description}

        You may encourage the the following actions:
        {COMMANDS}

        You ascribe to the following values:
        {self.values}
        """
        
    def get_response(self, user_input):
        self.messages.append({'role': 'user', 'content': user_input})
        
        response = openai_request(
            model=self.model,
            messages=self.messages
        )
        text = response.choices[0].message.content.strip()
        self.messages.append({'role': 'assistant', 'content': text})
        return text

    def print_debug_info(self):
        print("Model Debug Information:")
        print("Description:")
        print(f"  {self.description}")
        print("Actions:")
        for action in self.actions:
            print(f"  - {action}")
        print("Values:")
        for value in self.values:
            print(f"  - {value}")
        print("References:")
        print(f"  {self.references}")
        print("Additional API Data:")
        print(f"  {self.additional_api_data}")

    
    # --- Commands ---
    
    def c(self):
        print('Describe your task')
        
        task_desc = input("> ")
        
        text = self.get_response(f'Break down this into a series of subtasks {task_desc}')
        
        while True:
            
            print(text)
            
            self.messages.append({'role': 'assistant', 'content': 'Does this look good? yes / no + explain why'})
            print(f'\nDoes this look good? yes / no + explain why')
            
            i = input("> ")
            
            if i == 'y' or i =='yes':
                break
            else:
                if len(i) > 2:
                    feedback_prompt = f"No. Please improve tasks based on feedback: {i}"
                else:
                    feedback_prompt = "No, please make these tasks more clear"
                text = self.get_response(feedback_prompt)
                
        while True:
            
            break
            
# --- Execute ---

def initialize():
    global master
    master = Kik('master')
    master.print_debug_info()

# Updates all files at the end of session.
def end_session():
  # Updates vocabulary.yaml and kik index.yamls based on kiks

  end_message = "\nThank you for coming to bmo.cafe. Goodbye!"
  print(end_message)

def get_lexicon_tasks():
    lexicon_path = 'lexicon.yaml'
    # Read the current contents of the lexicon file
    with open(lexicon_path, 'r') as file:
        lexicon_data = yaml.safe_load(file)
    # Return the tasks if they exist and are not empty
    if 'tasks' in lexicon_data and lexicon_data['tasks']:
        return lexicon_data['tasks']
    else:
        return None

def l():
    print("Existing tasks:")
    
    tasks = get_lexicon_tasks()
    
    if tasks is not None:
        for task in tasks:
            for task_name, task_description in task.items():
                print(f"- {task_name}: {task_description}")
    else:
        print("No tasks found in the lexicon.")
    
def g():
    print("Let's generate a new task! Please describe it:")
    
    task_desc = input("< ")
    # Generate name of task
    task_name = master.get_response(f"""
Help to generate a new task for a program. 
The user provided this description of the task: {task_desc}
Please generate a short name for this task, using only lowercase letters, numbers and underscores. For example, "hello_world". Reply ONLY with the short name.
""")
    
    #  Make directory for task
    os.makedirs(f"tasks/{task_name}")
    
    # Create config.yaml
    task_desc = master.get_response(f'Clean up this task description so it is grammatically correct and in complete sentences: {task_desc}')
    with open(f"tasks/{task_name}/config.yaml", "w") as f:
        f.write(f"""description: {task_desc}
generated_with:
  type: ai
  model: {master.model}
""")
        
    # Create program
    code, test_set = generate_task(task_name, task_desc)
    with open(f"tasks/{task_name}/index.py", "w") as f:
        f.write(code)
    # Write tests to tests.csv
    with open(f"tasks/{task_name}/tests.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['input', 'ideal_output'])  # Write header
        for test in test_set:
            writer.writerow([test['input'], test['ideal_output']])

    print(f'Task {task_name} and its tests is successfully created!')
    
    update_lexicon()
    
    
def r(task_name):
    tasks = get_lexicon_tasks()
    if tasks and any(task_name in task for task in tasks):
        print(f"Running task: {task_name}")
        task_folder = f"tasks/{task_name}"
        if os.path.exists(task_folder):
            task_config_path = os.path.join(task_folder, "config.yaml")
            with open(task_config_path, 'r') as file:
                task_config = yaml.safe_load(file)
            print(f"Task description: {task_config['description']}")
            
            task_script_path = os.path.join(task_folder, "index.py")
            if os.path.exists(task_script_path):
                print(f"Executing script at {task_script_path}\n")
                
                spec = importlib.util.spec_from_file_location(task_name, task_script_path)
                task_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(task_module)
                task_function = getattr(task_module, task_name)
                
                if 'runtime' in task_config and task_config['runtime'].get('asyncio') is True:                
                    asyncio.run(task_function())
                else:
                    task_function()
                
            else:
                print(f"Task script not found at: {task_script_path}")
    else:
        print(f"Task '{task_name}' not found in the lexicon. Please provide a valid task_name.")
    
    
def t(task_name):
    tasks = get_lexicon_tasks()
    if tasks and any(task_name in task for task in tasks):
        task_folder = f"tasks/{task_name}"
        if os.path.exists(task_folder):
            task_script_path = os.path.join(task_folder, "index.py")
            task_tests_path = os.path.join(task_folder, "tests.csv")
            
            if os.path.exists(task_script_path) and os.path.exists(task_tests_path):
                print(f"Running tests for task: {task_name}")
                
                with open(task_tests_path, 'r') as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)  # Skip the header row
                    
                    result_file = os.path.join(task_folder, "results.csv")
                    with open(result_file, 'w') as file:
                        writer = csv.writer(file)
                        writer.writerow(['input', 'ideal_output', 'actual_output'])
                            
                    for row in csv_reader:
                        print(f"\nRunning test case: {row}")
                        input_value = row[0]
                        ideal_output = row[1]
                        
                        spec = importlib.util.spec_from_file_location(task_name, task_script_path)
                        task_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(task_module)
                        task_function = getattr(task_module, task_name)
                        actual_output = task_function(input_value)
                        
                        with open(result_file, 'a') as file:
                            writer = csv.writer(file)
                            writer.writerow([input_value, ideal_output, actual_output])
            else:
                if not os.path.exists(task_script_path):
                    print(f"Task script not found at: {task_script_path}")
                if not os.path.exists(task_tests_path):
                    print(f"Test cases not found at: {task_tests_path}")
        else:
            print(f"Task folder not found at: {task_folder}")
    else:
        print(f"Task '{task_name}' not found in the lexicon. Please provide a valid task_name.")
    
    
def s(task_name, schedule):
    if task_name is None:
        print("Please provide a task name to schedule.")
        return
    
    if schedule is None:
        print("Please provide a schedule (either 'daily' or a number of seconds) for the task.")
        return
    
    tasks = get_lexicon_tasks()
    if tasks and any(task_name in task for task in tasks):
        path = None
        if schedule.isdigit():
            seconds = int(schedule)
            print(f"Scheduling task '{task_name}' to run every {seconds} seconds.")
            path = schedule_task(task_name, None, seconds)
        else:
            print(f"Scheduling task '{task_name}' to run daily at 8pm PT.")
            path = schedule_task(task_name, 'daily')
        check_scheduled_task(path)
    else:
        print(f"Task '{task_name}' not found in the lexicon. Please provide a valid task name.")
    
    
def a():
    print("Scheduled tasks:")
    os.system("launchctl list | grep com.bmocafe")



def main():
    
    initialize()

    print("""Welcome to bmo.cafe ☕️ How can I help you today?""")
    print(COMMANDS)

    while True:
        try:
            user_input = input("> ")
            user_input = user_input.lower()
            
            if user_input == 'l':
                l()
            elif user_input == 'g':
                g()
            elif user_input.startswith('r ') or user_input == 'r':
                task_name = user_input[2:]
                r(task_name)
            elif user_input.startswith('t ') or user_input == 't':
                task_name = user_input[2:]
                t(task_name)
            elif user_input.startswith('s ') or user_input == 's':
                task_name = user_input.split(' ')[1] if len(user_input.split(' ')) > 1 else None
                schedule = user_input.split(' ')[2] if len(user_input.split(' ')) > 2 else None
                s(task_name, schedule)
            elif user_input == 'a':
                a()
            elif user_input == 'q':
                end_session()
                break
            else:
                text_response = master.get_response(user_input)
                print(text_response)
                print(COMMANDS)
            
                # print('---')
                # print(f"Tokens and cost used for this request: {last_request_usage['input'] + last_request_usage['output']} tokens / ${round(last_request_usage['input_cost'] + last_request_usage['output_cost'], 4)}")
                
                # print(f"Tokens and cost used in total: {total_usage['input'] + total_usage['output']} tokens / ${round(total_usage['input_cost'] + total_usage['output_cost'], 4)}")
            
        except KeyboardInterrupt:
            end_session()
            break

        
if __name__ == "__main__":
    main()
