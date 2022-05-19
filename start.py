import os
from secrets import choice

# print("Choose a script to run:")
# print("1. Start the backend server")
# print("2. Start the frontend server")
# print("3. Start both servers")
# print("0. Exit")
# choice = input("Enter your choice: ")


def start_server():
    os.system(
        "cd venv && cd Scripts && activate && cd ../.. && python app.py")
