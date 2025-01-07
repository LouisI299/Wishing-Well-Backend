from flask_mail import Message
from app import mail  

def send_mail(subject, recipients, body):

    msg = Message(
        subject=subject,
        recipients=recipients,
        body=body,
        sender='wishing-well@team.com'
    )
    try:
        mail.send(msg)
        return "E-mail sent successfully"
    except Exception as e:
        return f"Error while trying to send email:  {str(e)}"
