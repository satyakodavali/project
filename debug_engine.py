import sys
import os
import sqlite3

# Add backend to path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.append(backend_path)

from chatbot.engine import get_student_data

def manual_test():
    roll = "22CSE101"
    query = "show my backlogs"
    print(f"Testing with Roll: {roll}, Query: {query}")
    try:
        response = get_student_data(roll, query)
        print("--- RESPONSE ---")
        print(response)
        print("--- END RESPONSE ---")
        
        # Verification
        assert "### Current Backlogs" in response
        assert "| Subject | Semester |" in response
        assert "With better performance in upcoming exams, you can easily improve" in response
        assert "### NOTE" in response
        assert "Your backlog exam" in response
        
        print("Verification successful!")
    except Exception as e:
        print(f"Execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    manual_test()
