import sqlite3
from werkzeug.security import check_password_hash

db_path = r'c:\Users\LENOVO\NewCollegeChatBot\college-portal\backend\nsrit_portal.db'

def verify_hash():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    roll_no = "24CSE100"
    cursor.execute("SELECT password_hash FROM students WHERE roll_no = ?", (roll_no,))
    row = cursor.fetchone()
    
    if row:
        pw_hash = row[0]
        passwords_to_test = ["Pass123!", "24CSE100", "admin", "password", "NSRIT@123"]
        print(f"Roll No: {roll_no}")
        print(f"Hash in DB: {pw_hash}")
        
        for pwd in passwords_to_test:
            is_correct = check_password_hash(pw_hash, pwd)
            print(f"Password '{pwd}' is correct: {is_correct}")
    else:
        print(f"Roll No {roll_no} not found.")
        
    conn.close()

if __name__ == "__main__":
    verify_hash()
