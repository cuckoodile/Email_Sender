# emailer.py
import os
import smtplib
from email.message import EmailMessage
from enum import Enum
from typing import List, Optional

class EmailStatus(Enum):
    SENT = "sent"
    FAILED = "failed"
    NOT_FOUND = "not_found"
    CONNECTION_ERROR = "connection_error"
    OTHER_ERROR = "other_error"


class EmailSender:
    def __init__(self):
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.password = os.getenv("SENDER_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

        if not self.sender_email or not self.password:
            raise ValueError("SENDER_EMAIL and SENDER_PASSWORD must be set in .env file")

    def send_single_email(self, receiver_email: str, subject: str, html_content: str, text_content: str = "", attachment_path: str = None):
        """
        Send a single email to the specified recipient
        """
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.sender_email
        msg["To"] = receiver_email

        # Add both HTML and plain text content
        if text_content:
            msg.set_content(text_content)
        msg.add_alternative(html_content, subtype="html")

        # Add attachment if provided
        if attachment_path:
            import os
            from email.mime.base import MIMEBase
            from email import encoders

            # Extract file name from path
            filename = os.path.basename(attachment_path)

            # Open and attach the file
            with open(attachment_path, "rb") as attachment:
                # Instance of MIMEBase and named as part
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}',
            )

            # Attach the part to message
            msg.attach(part)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.send_message(msg)
            return {"status": EmailStatus.SENT, "message": "Email sent successfully"}
        except smtplib.SMTPRecipientsRefused:
            return {"status": EmailStatus.NOT_FOUND, "message": f"Recipient {receiver_email} not found"}
        except smtplib.SMTPServerDisconnected:
            return {"status": EmailStatus.CONNECTION_ERROR, "message": "Connection to SMTP server failed"}
        except smtplib.SMTPException as e:
            return {"status": EmailStatus.OTHER_ERROR, "message": f"SMTP error: {str(e)}"}
        except Exception as e:
            return {"status": EmailStatus.OTHER_ERROR, "message": f"Failed to send email: {str(e)}"}

    def send_bulk_emails(self, receivers: List[str], subject: str, html_content: str, text_content: str = "", attachment_path: str = None):
        """
        Send emails to multiple recipients and return the status for each
        """
        results = []
        for receiver in receivers:
            result = self.send_single_email(receiver, subject, html_content, text_content, attachment_path)
            results.append({
                "email": receiver,
                "status": result["status"],
                "message": result["message"]
            })
        return results
