from models.oai import gpt
import json

def generate_code(prompt: str):
  '''
  This function uses a language model to generate code based on the prompt.
  Example: """
    def solve_task(input):
      # Example solution logic
      return input * 2
  """
  '''
  tries = 0
  while tries < 5:
    code = gpt('gpt-4-0613', prompt)
    try:
      exec(code)
      print(f'Try #{tries+1} to generate code SUCCESS: {code}')
      return code
    except SyntaxError:
      print(f'Try #{tries+1} generate code FAIL: {code} \n Trying again.')
      tries += 1

  raise Exception(f"Failed to generate code after {tries} attempts :(")
          
# Placeholder function to simulate language model's test set generation
def generate_test_set(prompt: str):
  '''
  This function uses a language model to generate test sets based on the prompt
  Example: [
    {'input': 10, 'ideal_output': 20},
    {'input': 5, 'ideal_output': 10},
  ]
  '''
  tries = 0
  while tries < 5:
    tests = gpt('gpt-4-0613', prompt)
    try:
        test_set = json.loads(tests)
    except json.decoder.JSONDecodeError:
        print(f'Try #{tries+1} generate test_set FAIL: model answer {tests} is not a list. \n Trying again.')
        tries += 1
        continue

    if all(isinstance(i, dict) and 'input' in i and 'ideal_output' in i and isinstance(i['input'], (int, float)) and isinstance(i['ideal_output'], (int, float)) for i in test_set):
      print(f'Try #{tries+1} to generate test_set SUCCESS: {test_set}')
      return test_set
    else:
      print(f'Try #{tries+1} generate test_set FAIL: {test_set} \n Trying again.')
    
    tries += 1
  raise Exception(f"Failed to generate a valid test set after {tries} attempts :(")

# Function to evaluate the generated code against the test set
def evaluate_code(task_name, code, test_set):
  # Define a local scope to execute the generated code
  local_scope = {}
  exec(code, globals(), local_scope)
  solve_task = local_scope[task_name]

  # Iterate over each test case in the test set
  for test in test_set:
    input_val = test['input']
    ideal_output = test['ideal_output']
    actual_output = solve_task(input_val)
    
    # Check if the actual output matches the expected output
    if actual_output != ideal_output:
        return False  # Test failed
  return True  # All tests passed

# Main loop to generate code and test sets until a solution passes all tests
def generate_task(task_name, task_description):
  max_iterations = 10  # Limit the number of iterations to prevent infinite loops
  num_tests = 2
  for iteration in range(max_iterations):
    # Generate code and test set based on the task description
    code_prompt = f"Generate Python function to {task_description}. DO NOT ADD COMMENTS OR TESTS.Only return the function named {task_name} with a single input parameter of type int, 'input' and single output parameter of type int. Your raw response should be executable as code." 
    test_prompt = f"Generate test set for task: {task_description}. Your result should be a python list of length {num_tests} where each item is an object with 'input' parameter of type int and 'ideal_output' field of type int. Every object should have a different input. Your raw response MUST be parseable as a list in python with json.loads"
    
    generated_code = generate_code(code_prompt)
    generated_test_set = generate_test_set(test_prompt)
    
    # Evaluate the generated code against the generated test set
    if evaluate_code(task_name, generated_code, generated_test_set):
      print(f"Solution found in iteration {iteration+1}")
      print(generated_code)
      return generated_code, generated_test_set
    else:
      print(f"Solution failed in iteration {iteration+1}. \n Trying again...")
  
  print("Failed to find a solution within the iteration limit.")
  return None, None


def main():
  task_name = "add_two_numbers"
  task_description = "Write a python function that adds two numbers"
  generate_task(task_name, task_description)
    
if __name__ == "__main__":
    main()
