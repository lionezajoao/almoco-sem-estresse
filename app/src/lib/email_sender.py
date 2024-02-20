import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import os
load_dotenv()

class EmailSender:
    def __init__(self, use_tls=True):
        self.host = os.getenv('SMTP_HOST')
        self.port = os.getenv('SMTP_PORT')
        self.username = os.getenv('SMTP_USERNAME')
        self.password = os.getenv('SMTP_PASSWORD')
        self.use_tls = use_tls

    def send_text_email(self, subject, recipients, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = ', '.join(recipients)

        self.send_email(msg)

        

    def send_media_email(self, subject, recipients, attachment_path):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = ', '.join(recipients)

        with open(attachment_path, 'rb') as file:
            part = MIMEApplication(file.read(), Name=attachment_path.split("/")[-1])
            part['Content-Disposition'] = f'attachment; filename="{ attachment_path.split("/")[-1] }"'
            msg.attach(part)

        self.send_email(msg)

    def send_email(self, msg):
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(self.username, self.password)
                smtp_server.send_message(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {str(e)}")

        

    def generate_stylized_email_body(self):
        # HTML header with styling
        return """
        <html>
            <head>
                <style>
                    body {font-family: Arial, sans-serif;}
                    table {border-collapse: collapse; width: 100%;}
                    th, td {border: 1px solid #ddd; text-align: left; padding: 8px;}
                    th {background-color: #f2f2f2;}
                    .shopping-list {margin-top: 20px;}
                    .category {background-color: #f2f2f2; font-weight: bold;}
                    .attachment-notice {margin-top: 20px; font-weight: bold; color: red;}
                </style>
            </head>
            <body>
                <div class="attachment-notice">
                    <p>Olá! Seu menu está pronto! Basta baixar o arquivo Excel atrelado a este email.</p>
                </div>
        """
