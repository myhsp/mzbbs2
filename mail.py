from flask_mail import Message
from threading import Thread

def async_send_email(app, mail, msg):
    mail.send(msg)

def send_email(app,mail,subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=async_send_email, args=(app,mail, msg)).start()
