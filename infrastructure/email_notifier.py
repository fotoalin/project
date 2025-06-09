# infrastructure/email_notifier.py
import logging

from services.interfaces import Notifier

logger = logging.getLogger(__name__)


def send_mail(subject, message, from_email, recipient_list):
    """Mock send_mail function for demonstration purposes"""
    logger.info("Sending email:")
    logger.info(f"  Subject: {subject}")
    logger.info(f"  From: {from_email}")
    logger.info(f"  To: {recipient_list}")
    logger.info(f"  Message: {message}")
    print(f"📧 Email sent to {recipient_list}: {subject}")
    return True


def send_sms(message, recipient):
    """Mock send_sms function for demonstration purposes"""
    logger.info(f"Sending SMS to {recipient}: {message}")
    print(f"📱 SMS sent to {recipient}: {message}")
    return True


class EmailNotifier(Notifier):
    def send(self, message: str, recipient: str) -> None:
        send_mail("Lead Notification", message, "noreply@example.com", [recipient])


class SMSNotifier(Notifier):
    def send(self, message: str, recipient: str) -> None:
        send_sms(message, recipient)
