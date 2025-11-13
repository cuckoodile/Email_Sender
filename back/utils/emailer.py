import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).with_name(".env")
load_dotenv(dotenv_path=env_path)

# Configuration
sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("SENDER_PASSWORD")
receiver_email = "sample@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Create message
msg = EmailMessage()
msg["Subject"] = "Customized Email from Python"
msg["From"] = sender_email
msg["To"] = receiver_email

# HTML body with customizations
html_content = """
<html>
<body>
    <h1 style="color: pink; font-family: Arial;">Custom Header (Blue, Arial)</h1>
    <p>This is <b>bold</b> text in <i>italics</i>, size 16px, red color: 
       <span style="color: red; font-size: 16px; font-family: Times New Roman;">Custom styled text!</span></p>
    <p>Large green font: <font size="5" color="green">Big and Green</font></p>
    <p>Using CSS class (define in <style>): <span class="highlight">Highlighted!</span></p>
</body>
</html>
"""
msg.add_alternative(html_content, subtype="html")  # Set as HTML

# Send via SMTP
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()  # Enable TLS
    server.login(sender_email, password)
    server.send_message(msg)

print("Email sent successfully!")