import sys
import os
import unittest
from flask import Flask

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from routes.chatbot_routes import chatbot_bp


class TestRealEmailOTP(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test'

        # 🔥 IMPORTANT: Add your real config here
        self.app.config['MAIL_USERNAME'] = 'nsritcollege@gmail.com'
        self.app.config['MAIL_PASSWORD'] = 'rkhulofnzylgqqpk'

        self.app.register_blueprint(chatbot_bp)
        self.client = self.app.test_client()

    def test_real_email_otp(self):

        print("\n🔄 Sending OTP to real email...\n")

        response = self.client.post(
            '/parent/request-otp',   # ⚠️ change if you have prefix
            json={'roll_no': '24CSE100'}
        )

        print("Response:", response.get_json())

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data['status'], 'success')

        print("\n✅ Check your Gmail inbox NOW!\n")


if __name__ == '__main__':
    unittest.main()
