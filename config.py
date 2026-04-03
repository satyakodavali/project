import os

class Config:
    SECRET_KEY = 'nsrit-super-secret-key-2024'

    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True

    SQLALCHEMY_DATABASE_URI = r'sqlite:///c:\Users\LENOVO\NewCollegeChatBot\college-portal\backend\nsrit_portal.db'

    # ✅ EMAIL CONFIG (REAL)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    MAIL_USERNAME = 'nsritcollege2002@gmail.com'
    MAIL_PASSWORD = 'mtvcatwysgaozuxs'   # ✅ App Password only