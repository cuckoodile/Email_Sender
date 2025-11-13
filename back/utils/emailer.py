# emailer.py
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("SENDER_PASSWORD")
receiver_email = "milo@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587

if not sender_email or not password:
    raise ValueError("SENDER_EMAIL and SENDER_PASSWORD must be set in .env file")

msg = EmailMessage()
msg["Subject"] = "Customized Email from Python"
msg["From"] = sender_email
msg["To"] = receiver_email

html_content = """
<html>
<body>
    <h1 style="color: pink; font-family: Arial;">Custom Header (Pink, Arial)</h1>
    <p>This is <b>bold</b> text in <i>italics</i>, size 16px, red color: 
       <span style="color: red; font-size: 16px; font-family: Times New Roman;">Custom styled text!</span></p>
    <p>Large green font: <span style="font-size: 20px; color: green;">Big and Green</span></p>
    <p>Using CSS class: <span class="highlight">Highlighted!</span></p>

    <style>
        .highlight {
            background-color: yellow;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: bold;
        }
    </style>
</body>
</html>
"""
msg.add_alternative(html_content, subtype="html")

# === Send email ===
try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")