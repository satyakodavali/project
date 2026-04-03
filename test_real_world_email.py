import sys
import os

# Add backend to path
backend_path = r'c:\Users\LENOVO\NewCollegeChatBot\college-portal\backend'
sys.path.append(backend_path)

from flask import Flask
from utils.email_service import send_email_otp
from config import Config

def test_real_email():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    with app.app_context():
        # Test with one of the provided emails
        test_recipient = "navadeepreyyi1419@gmail.com"
        test_otp = "123456"
        test_name = "Real World Test Student"
        
        print(f"Attempting to send real OTP email to {test_recipient}...")
        try:
            success = send_email_otp(test_recipient, test_otp, test_name)
            
            if success:
                print("SUCCESS: Real-world email delivery verified!")
            else:
                print("FAILURE: send_email_otp returned False.")
        except Exception as e:
            print(f"CRITICAL FAILURE: An exception occurred during send_email_otp: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_real_email()
