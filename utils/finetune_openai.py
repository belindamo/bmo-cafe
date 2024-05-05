# This is only called once. It's added here for record.
# This finetunes on GSM8K using OpenAI's fine-tuning API

import json
from openai import OpenAI
client = OpenAI()

# --- CLEAN DATA ---

# Open the original file and create a new file for the output
# with open('../datasets/GSM8K/train.jsonl', 'r') as infile, open('converted_train.jsonl', 'w') as outfile:
#     for line in infile:
#         # Load the JSON object from the line
#         data = json.loads(line)
        
#         # Extract the question and answer
#         question = data.get('question', '')
#         answer = data.get('answer', '')
        
#         # Create the new format
#         new_data = {
#             "messages": [
#                 {"role": "user", "content": question},
#                 {"role": "assistant", "content": answer}
#             ]
#         }
        
#         # Write the new JSON object to the output file
#         outfile.write(json.dumps(new_data) + '\n')


# --- ADD FILE ---

# client.files.create(
#   file=open("../datasets/GSM8K/train_finetune_openai_100.jsonl", "rb"),
#   purpose="fine-tune"
# )

# client.files.create(
#   file=open("../datasets/GSM8K/train_finetune_openai_7473.jsonl", "rb"),
#   purpose="fine-tune"
# )

# --- FINETUNE ---

# 100 file-0GhSNITh6KjZ4Wekdi1VR3ud
# 1000 file-9WRvmlyXU83IQWm7giL6g1Do
# 7473 file-bZznB6aVvNU2d7PLTIAbMj47

# for 3.5
# client.fine_tuning.jobs.create(
#   training_file="file-bZznB6aVvNU2d7PLTIAbMj47", 
#   model="gpt-3.5-turbo"
# )
