import requests
import time

BASE_URL = "http://localhost:5000/api/chatbot"
session = requests.Session()

def test_api_flow():
    # 1. Request OTP for a roll number that has a seeded email
    # Let's use 24CSE100 which we know is seeded (or another one)
    # We can fetch a roll number from the db directly that has sanjupedaprolu@gmail.com
    import sqlite3
    conn = sqlite3.connect(r'c:\Users\LENOVO\NewCollegeChatBot\college-portal\backend\nsrit_portal.db')
    cursor = conn.cursor()
    cursor.execute("SELECT roll_no, parents_email FROM students WHERE parents_email = 'sanjupedaprolu@gmail.com' LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        print("No student found with the target email.")
        return
        
    roll_no = row[0]
    email = row[1]
    
    print(f"--- Step 1: Requesting OTP for Roll No: {roll_no} (Email: {email}) ---")
    
    # Request OTP
    res1 = session.post(f"{BASE_URL}/parent/request-otp", json={"roll_no": roll_no})
    data1 = res1.json()
    print("Response payload:", data1)
    
    if data1.get("status") != "success":
        print("Failed to request OTP.")
        return
        
    # Since we are sending a real email, we can't fetch the OTP from the response if it doesn't return it
    # But wait, in our modified chatbot_routes.py we might not be returning the OTP anymore. 
    # Let's check the console logs for the OTP. 
    # Actually, we can just read the OTP from the flask session or log, but it's simpler to test verify-otp if we know it.
    # To reliably test it automatically, let's temporarily fetch the OTP from the backend print or let the user check their email!
    print(f"\n✅ OTP has been sent via REAL EMAIL to {email}!")
    print(f"The backend log will show: [OTP DEBUG] OTP XXXXXX for student ...")
    print("Please check the terminal where `python app.py` is running to see the OTP, or check the inbox.")

if __name__ == "__main__":
    test_api_flow()
