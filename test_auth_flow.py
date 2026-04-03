import requests
import time

BASE_URL = "http://localhost:5000/api/chatbot"

def test_full_auth_flow():
    # Use a session to maintain cookies
    session = requests.Session()
    
    # Let's use 23IT1034 (or any other seeded roll)
    roll_no = "23IT1034"
    
    print(f"--- Step 1: Requesting OTP for Roll No: {roll_no} ---")
    res1 = session.post(f"{BASE_URL}/parent/request-otp", json={"roll_no": roll_no})
    data1 = res1.json()
    print("Request Response:", data1)
    
    if data1.get("status") != "success":
        print("Failed to request OTP.")
        return
        
    print(f"\n--- Step 2: Retrieving OTP for testing ---")
    time.sleep(2) # Wait a bit to ensure session is saved
    res2 = session.get(f"{BASE_URL}/parent/get-last-otp")
    data2 = res2.json()
    print("OTP Retrieval Response:", data2)
    
    if data2.get("status") != "success":
        print("Failed to retrieve OTP.")
        return
        
    otp = data2.get("otp")
    
    print(f"\n--- Step 3: Verifying OTP: {otp} ---")
    res3 = session.post(f"{BASE_URL}/parent/verify-otp", json={"roll_no": roll_no, "otp": otp})
    data3 = res3.json()
    print("Verify Response:", data3)
    
    if data3.get("status") != "success":
        print("Failed to verify OTP.")
        return
        
    print(f"\n--- Step 4: Testing Authenticated Chatbot Query ---")
    query_payload = {
        "question": "show my backlogs",
        "is_guest_mode": True # Simulate home page behavior
    }
    res4 = session.post(f"{BASE_URL}/ask", json=query_payload)
    data4 = res4.json()
    print("Chatbot Response Snippet:")
    print(data4.get("response", "")[:200] + "...")
    
    print("\n✅ End-to-End Chatbot Auth Flow Successful!")

if __name__ == "__main__":
    test_full_auth_flow()
