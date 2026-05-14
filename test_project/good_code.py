import os
import sys

def hello_cat(name):
    print(f"Hello, {name}!")

def read_file(filepath):
    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return None
    
def greet_user(name):
    message = f"Hello {name}, nice to meet you!"
    return message

greeting = greet_user(input("Enter your name: "))
print(greeting)