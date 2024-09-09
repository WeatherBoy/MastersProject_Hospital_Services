# Test how the .env file (created in the project root DIR) works
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the .env file

username = os.getenv("USERID")
password = os.getenv("PASSWORD")
department = os.getenv("DEPARTMENT")

print(username, password, department)
