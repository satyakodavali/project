import requests
from flask import current_app

def send_sms(phone_number, message):
    """
    Sends an SMS using Fast2SMS API (common in India).
    To use this, you need a Fast2SMS API Key from https://www.fast2sms.com/
    """
    api_key = current_app.config.get('SMS_API_KEY')
    
    if not api_key or api_key == 'YOUR_FAST2SMS_KEY_HERE':
        print(f"\n[SMS MOCK] Real-world SMS sending skipped (No API Key).")
        print(f"[SMS MOCK] To {phone_number}: {message}\n")
        return False

    url = "https://www.fast2sms.com/dev/bulkV2"
    
    payload = {
        "variables_values": message.split()[-1], # Assuming the OTP is the last word
        "route": "otp",
        "numbers": phone_number,
    }
    
    # Alternatively, use the 'message' route if it's a custom text
    # payload = {
    #     "message": message,
    #     "language": "english",
    #     "route": "q",
    #     "numbers": phone_number,
    # }

    headers = {
        'authorization': api_key,
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }

    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        print(f"[SMS LOG] Fast2SMS Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"[SMS ERROR] Failed to send SMS: {e}")
        return False
