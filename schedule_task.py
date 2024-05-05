import os

def schedule_task(folder_name, interval_type, interval_value):
    # Construct the path to the index.py file within the specified folder
    index_py_path = os.path.expanduser(os.path.abspath(os.path.join('tasks', folder_name, 'index.py')))
    
    # Define the path for the plist file and check if it already exists
    base_plist_path = os.path.expanduser(f'~/Library/LaunchAgents/com.bmocafe.{folder_name}')
    plist_path = f"{base_plist_path}_0.plist"
    counter = 0
    while os.path.exists(plist_path):
        counter += 1
        plist_path = f"{base_plist_path}_{counter}.plist"
    
    log_path = os.path.expanduser(os.path.abspath(os.path.join('tasks', folder_name, 'streams', f'{counter}.log')))
    streams_folder_path = os.path.abspath(os.path.expanduser(os.path.join('tasks', folder_name, 'streams')))
    if not os.path.exists(streams_folder_path):
        os.makedirs(streams_folder_path)
        print(f"Streams folder created at: {streams_folder_path}")
    print(f"Attempting to write log to: {log_path}")
    if not os.path.exists(log_path):
        with open(log_path, 'w') as f:
            f.write("Log file created.\n")
        print("Log file created and written successfully")
    else:
        with open(log_path, 'a') as f:
            f.write("Test log entry")
        print("Log written successfully")
    
    # Define the job configuration for launchd
    if interval_type == 'daily':
        job = f"""
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>{plist_path.replace('.plist', '')}</string>
            <key>ProgramArguments</key>
            <array>
                <string>/usr/bin/python3</string>
                <string>{index_py_path}</string>
            </array>
            <key>StandardOutPath</key>
            <string>{log_path}</string>
            <key>StandardErrorPath</key>
            <string>{log_path}</string>
            <key>StartCalendarInterval</key>
            <dict>
                <key>Hour</key>
                <integer>20</integer>
                <key>Minute</key>
                <integer>0</integer>
            </dict>
        </dict>
        </plist>
        """
    else:
        job = f"""
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>{plist_path.replace('.plist', '')}</string>
            <key>ProgramArguments</key>
            <array>
                <string>/usr/bin/python3</string>
                <string>{index_py_path}</string>
            </array>
            <key>StandardOutPath</key>
            <string>{log_path}</string>
            <key>StandardErrorPath</key>
            <string>{log_path}</string>
            <key>StartInterval</key>
            <integer>{interval_value}</integer>
        </dict>
        </plist>
        """
    
    # Write the job configuration to the plist file
    with open(plist_path, 'w') as f:
        f.write(job)
    
    # Load the job into launchd
    os.system(f'launchctl load {plist_path}')
    
    return plist_path

# Function to check if the scheduled job is loaded
def check_scheduled_task(task_path):
    job_label = task_path.replace('.plist', '')
    # Execute the command and capture the output
    output = os.popen(f'launchctl list | grep {job_label}').read()
    # Check if the job label is in the output
    if job_label in output:
        print(f"Job {job_label} is successfully scheduled.")
    else:
        print(f"Job {job_label} is not scheduled.")

if __name__ == "__main__":

  # Call the function to schedule a task
  # task_1_path = schedule_task('pay_sf_parking_tickets', 'daily', None)  # Example for daily at 8pm
  task_2_path = schedule_task('hello_world', None, 10)  # Example for every 10 seconds

  # Check if the job for 'pay_sf_parking_tickets' is scheduled
  # check_scheduled_job(task_1_path)
  check_scheduled_task(task_2_path)
