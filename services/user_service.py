from email.headerregistry import Address
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from dotenv import load_dotenv
from flask import render_template
import os
from models import User
from repository.user_repository import user_repository


class UserService:

    def __init__(self):
        load_dotenv()

    def create_user(self, email):
        user = User(email=email)
        return user_repository.save_user(user)

    def send_email_updates(self, updates):
        from app import app
        with app.app_context():
            emails=self.get_users_email()
            self.send_email(subject='[Financers] Assets update',
                            sender='Financers<'+os.environ['MAIL_USERNAME']+'>',
                            recipients=emails,
                            html_body=render_template('email/email_update.html',
                                                    updates=updates))

    def send_email(self, subject, sender, recipients, html_body):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ','.join(recipients)
        msg.attach(MIMEText(html_body, 'html'))
        smtp = SMTP(os.environ['MAIL_SERVER'], os.environ['MAIL_PORT'])
        smtp.ehlo()
        smtp.starttls()
        smtp.login(os.environ['MAIL_USERNAME'], os.environ['MAIL_PASSWORD'])
        smtp.sendmail(sender, recipients, msg.as_string())

    def get_users_email(self):
        return user_repository.get_user_emails()


user_service = UserService()