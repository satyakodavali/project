import urllib.request
import json
import http.cookiejar

# Setup cookie handler for session persistence
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def post_json(url, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    with opener.open(req) as response:
        return response.getcode(), json.loads(response.read().decode('utf-8'))

try:
    # Request OTP
    print("Requesting OTP for 24CSE100...")
    status, res = post_json("http://localhost:5000/api/chatbot/parent/request-otp", {"roll_no": "24CSE100"})
    print(f"Status: {status}")
    print(f"Response: {res}")
    
    if status == 200:
        otp = res.get('otp')
        
        # Verify OTP
        print("\nVerifying OTP...")
        v_status, v_res = post_json("http://localhost:5000/api/chatbot/parent/verify-otp", {"roll_no": "24CSE100", "otp": otp})
        print(f"Status: {v_status}")
        print(f"Response: {v_res}")
        
except Exception as e:
    print(f"Error: {e}")
