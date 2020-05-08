import os

class  Config:
    SECRET_KEY = str(os.environ.get("SECRET"))
    SQLALCHEMY_DATABASE_URI = str(os.environ.get("DATABASE_URI"))



            # Resolute smtp = smtp.cacc.local
    MAIL_SERVER = os.environ.get("SMTP_ADDRESS")
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get("MAIL_USER")
    MAIL_PASSWORD = os.environ.get("MAIL_PASS")
