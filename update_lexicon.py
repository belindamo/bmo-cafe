import yaml
import os 

def update_lexicon():
    tasks_folder = 'tasks'
    lexicon_path = 'lexicon.yaml'
    
    # Read the current contents of the lexicon file
    with open(lexicon_path, 'r') as file:
        lexicon_data = yaml.safe_load(file)
    
    # Check if 'tasks' key exists, if not create one
    if 'tasks' not in lexicon_data or lexicon_data['tasks'] is None:
        lexicon_data['tasks'] = []
    
    # Iterate over each folder in the tasks folder
    new_tasks = []
    for task_folder in os.listdir(tasks_folder):
        task_path = os.path.join(tasks_folder, task_folder)
        
        # Check if it's a directory
        if os.path.isdir(task_path):
            task_name = task_folder
            config_path = os.path.join(task_path, 'config.yaml')
            
            # Check if config.yaml exists in the task folder
            if os.path.exists(config_path):
                with open(config_path, 'r') as config_file:
                    config_data = yaml.safe_load(config_file)
                    task_description = config_data.get('description', '')
                
                # Append the task to the lexicon
                new_tasks.append({task_name: task_description})
            
    lexicon_data['tasks'] = new_tasks
    
    # Write the updated data back to the lexicon file
    with open(lexicon_path, 'w') as file:
        yaml.safe_dump(lexicon_data, file, default_flow_style=False)



if __name__ == "__main__":
  update_lexicon()