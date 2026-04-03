import requests

BASE_URL = "http://localhost:5000"

def test_otp_flow():
    session = requests.Session()

    roll_no = input("Enter Roll Number: ")

    res = session.post(f"{BASE_URL}/api/chatbot/parent/request-otp", json={"roll_no": roll_no})
    data = res.json()
    print(data)

    if data['status'] == 'success':
        otp = input("Enter OTP received: ")

        res_v = session.post(f"{BASE_URL}/api/chatbot/parent/verify-otp",
                             json={"roll_no": roll_no, "otp": otp})
        print(res_v.json())

        question = input("Ask your question: ")

        res_a = session.post(f"{BASE_URL}/api/chatbot/ask",
                             json={"question": question})
        print(res_a.json())

if __name__ == "__main__":
    test_otp_flow()
