import requests
import json

base_url = "http://localhost:5000/api/auth" # Assuming it runs on 5000

def test_login(roll_no, password):
    url = f"{base_url}/login"
    payload = {
        "username": roll_no,
        "password": password,
        "type": "student"
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Login attempt for {roll_no}:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error connecting to backend: {e}")

if __name__ == "__main__":
    # Note: Backend must be running for this to work.
    # If not running, we can check the hash manually.
    test_login("24CSE100", "Pass123!")
