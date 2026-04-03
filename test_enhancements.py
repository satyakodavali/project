import sys
import os
import sqlite3

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from chatbot.predictions import cgpa_backlog_logic

def test_motivation():
    print("--- Testing Motivation Messages ---")
    res_low = cgpa_backlog_logic(7.5)
    print(f"CGPA 7.5 Motivation: {res_low['motivation']}")
    assert "close to 8 CGPA" in res_low['motivation']
    
    res_high = cgpa_backlog_logic(8.5)
    print(f"CGPA 8.5 Motivation: {res_high['motivation']}")
    assert "CGPA is good" in res_high['motivation']
    print("Motivation tests passed!\n")

def test_backlog_format():
    print("--- Testing Backlog Response Formatting ---")
    db_path = r'c:\Users\LENOVO\NewCollegeChatBot\college-portal\backend\nsrit_portal.db'
    if not os.path.exists(db_path):
        print(f"DB not found at {db_path}. Skipping DB-dependent tests.")
        return
        
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    from chatbot.engine import get_student_data
    
    # Using a roll number that has low CGPA (e.g., 22CSE1097 which is in 3-1 according to my previous search)
    # Wait, 24CSE100 is in 1-1, so it won't have PREVIOUS semesters.
    # Let's use 22CSE1097.
    response = get_student_data("22CSE1097", "show my backlogs")
    print(f"--- FULL RESPONSE START ---\n{response}\n--- FULL RESPONSE END ---")
    
    # 1. No CGPA prediction line
    assert "Prediction:" not in response
    assert "Your current CGPA is" not in response
    
    # 2. Fixed motivation
    # User requirement: "With better performance in upcoming exams, you can easily improve. Focus on weak subjects and practice regularly."
    assert "With better performance in upcoming exams, you can easily improve" in response
    
    # 3. Table format
    assert "| Subject | Semester |" in response
    
    # 4. NOTE section
    assert "### NOTE" in response
    
    print("Backlog formatting tests passed!\n")

if __name__ == "__main__":
    try:
        test_motivation()
        test_backlog_format()
        print("All verification tests passed successfully!")
    except Exception as e:
        print(f"Tests failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
