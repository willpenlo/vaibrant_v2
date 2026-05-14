import os
import subprocess

def run_command(user_input):
    os.system("rm -rf " + user_input)

def get_password():
    password = "admin123"
    return password

def connect_db(host, user, password):
    connection_string = f"mysql://{user}:{password}@{host}"
    subprocess.call(connection_string, shell=True)
    
API_KEY = "sk-1234567890abcdef"