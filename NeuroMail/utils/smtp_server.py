import os
import smtplib
from django.conf import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

SMTP_SERVER = settings.MAIL_SERVER
SMTP_PORT = 587  # Use 587 for TLS, 465 for SSL


def send_email(
    subject,
    body,
    from_email,
    password,
    recipients,
    attachments=[],
):
    """
    Send an email with the given subject, body, and attachments.
    """

    msg = MIMEMultipart(
        "alternative"
    )  # Set alternative to send both plain text and HTML
    msg["From"] = from_email
    msg["Subject"] = subject

    def get_emails(filter_type):
        return [
            recipient["email"]
            for recipient in recipients
            if recipient["recipient_type"] == filter_type
        ]

    # Set the 'To', 'Cc', and handle 'Bcc' separately
    to_emails = get_emails("to")
    cc_emails = get_emails("cc")
    bcc_emails = get_emails("bcc")

    all_emails = to_emails + cc_emails + bcc_emails

    msg["To"] = ", ".join(to_emails)
    msg["Cc"] = ", ".join(cc_emails)

    # Attach plain text version (fallback)
    plain_body = body.strip()  # In case you want to handle plain text
    msg.attach(MIMEText(plain_body, "plain"))

    # Attach HTML version
    msg.attach(MIMEText(body, "html"))

    # Attach files if any
    if attachments:
        for file_path in attachments:
            try:
                with open(file_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                    part["Content-Disposition"] = (
                        f'attachment; filename="{os.path.basename(file_path)}"'
                    )
                    msg.attach(part)
            except Exception as e:
                print(f"Failed to attach file {file_path}: {e}")

    try:
        # Connect to the server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Upgrade the connection to secure
        server.login(from_email, password)

        # Send the email to all recipients, including Bcc
        server.sendmail(from_email, all_emails, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()
