import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app


def send_email_otp(recipient_email, otp, student_name):
    try:
        mail_server = current_app.config.get('MAIL_SERVER')
        mail_port = current_app.config.get('MAIL_PORT')
        mail_username = current_app.config.get('MAIL_USERNAME')
        mail_password = current_app.config.get('MAIL_PASSWORD')

        # 🔥 Debug (optional)
        print("MAIL USER:", mail_username)

        subject = "OTP Verification - NSRIT Portal"
        body = f"""
Hello,

Your OTP for verification is: {otp}

Student: {student_name}

Do NOT share this OTP with anyone.

Regards,  
NSRIT Portal
"""

        msg = MIMEMultipart()
        msg['From'] = mail_username
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(mail_server, mail_port)
        server.starttls()
        server.login(mail_username, mail_password)

        server.sendmail(mail_username, recipient_email, msg.as_string())
        server.quit()

        print(f"[EMAIL SUCCESS] OTP sent to {recipient_email}")
        return True

    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False