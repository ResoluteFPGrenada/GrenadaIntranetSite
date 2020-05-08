import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from WebApp import mail
import smtplib
from email.message import EmailMessage

def send_log(message, log_type):
    log_path = os.path.join(current_app.root_path, 'static/logs/', log_type + '.log')
    file = open(log_path, 'a')
    file.write(message)
    file.write(os.linesep)
    file.close()

    # function for account page. saves uploaded images.
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/ProfilePics', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_email(receiver, message):
    sender = 'GrenadaIntranetSite@resolutefp.com'
    s = smtplib.SMTP('smtp.cacc.local')
    s.sendmail(sender, receiver, message)
    s.quit()

def send_reset_email(user):
    token = user.get_reset_token()
    #msg = EmailMessage()
    body = """MIME-Version: 1.0
Content-type: text/html
Subject: Grenada Intranet Password Reset
To Reset your password, visit the following link:
<a href="{}">Reset Password</a>

If you did not make this request then simply ignore this email and no changes will be made.
""".format(url_for('users.reset_token', token=token, _external=True))

    #msg.set_content(body)
    #msg['Subject'] = 'Test Email Subject'
    #msg['From'] = 'test@resolutefp.com'
    Sender = 'GrenadaIntranetSite@resolutefp.com'
    Receiver = user.email
    #msg['To'] = user.email
    s = smtplib.SMTP('smtp.cacc.local')
    s.sendmail(Sender, Receiver, body)
    s.quit()

def send_reset_email2(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made. 
'''
    mail.send(msg)
