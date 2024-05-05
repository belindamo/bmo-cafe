from datetime import datetime

def hello_world():
  # Print "hello world!" with the current date and time in a readable format
  print(f"Hello world! It is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
  hello_world()