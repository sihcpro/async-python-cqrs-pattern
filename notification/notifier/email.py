import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from ..base.notifier import Notifier
from ..cfg import config

smtp_host = os.environ.get("SMTP_HOST", config.SMTP_HOST)
smtp_port = os.environ.get("SMTP_PORT", config.SMTP_PORT)
smtp_user = os.environ.get("SMTP_USER", config.SMTP_USER)
smtp_pass = os.environ.get("SMTP_PASS", config.SMTP_PASS)


class EmailNotifier(Notifier):
    @staticmethod
    def send_smtp_email(
        recipients: list,
        subject,
        body,
        bcc: list = None,
        subtype="html",
        mime_charset="utf-8",
    ):
        smtp_client = smtplib.SMTP(host=smtp_host, port=int(smtp_port))
        smtp_client.starttls()
        smtp_client.login(smtp_user, smtp_pass)

        msg = MIMEMultipart()
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject
        msg["From"] = formataddr(("Bridging All Space", smtp_user))
        if bcc:
            msg["Bcc"] = ", ".join(bcc)

        msg.attach(MIMEText(body, subtype, mime_charset))

        smtp_client.send_message(msg)


# EmailNotifier.send_smtp_email(["tvquocchi@gmail.com"], "Hello", "Hello")
