import sys
import os

# Add the current directory to sys.path so we can import chatbot and utils
sys.path.append(os.getcwd())

from chatbot.engine import process_query

# Mock user context for Manasa Patel
user_context = {
    'role': 'student',
    'roll_no': '22CIVIL109',
    'name': 'Manasa Patel'
}

print("Testing 'When is my next mid exam?':")
print(process_query("When is my next mid exam?", user_context))

print("\nTesting 'When is my next semester exam?':")
print(process_query("When is my next semester exam?", user_context))

print("\nTesting 'exam dates':")
print(process_query("exam dates", user_context))
