import requests

url = "http://localhost:5000/api/chatbot/parent/request-otp"
data = {"roll_no": "24CSE100"}

try:
    response = requests.post(url, json=data)
    print("Requesting OTP for 24CSE100...")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        otp = response.json().get('otp')
        cookies = response.cookies
        
        # Verify OTP
        verify_url = "http://localhost:5000/api/chatbot/parent/verify-otp"
        verify_data = {"roll_no": "24CSE100", "otp": otp}
        verify_response = requests.post(verify_url, json=verify_data, cookies=cookies)
        
        print("\nVerifying OTP...")
        print(f"Status: {verify_response.status_code}")
        print(f"Response: {verify_response.json()}")
        
except Exception as e:
    print(f"Error: {e}")
