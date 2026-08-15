import smtplib
from email.message import EmailMessage


def send_email(sender_email, app_password, receiver_email, subject, message):
    try:
        email = EmailMessage()

        email["From"] = sender_email
        email["To"] = receiver_email
        email["Subject"] = subject

        email.set_content(message)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(email)

        return True

    except Exception as e:
        print("Email error:", e)
        return False