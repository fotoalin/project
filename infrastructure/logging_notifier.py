"""
Logging Notifier Implementation - demonstrates Open/Closed Principle

This shows how easy it is to add new notification channels without
modifying existing code. The logging notifier writes notifications
to log files instead of sending emails or SMS.
"""
import logging
from datetime import datetime

from services.interfaces import Notifier

# Configure a specific logger for notifications
notification_logger = logging.getLogger('notifications')
notification_logger.setLevel(logging.INFO)

# Create file handler if not already present
if not notification_logger.handlers:
    handler = logging.FileHandler('notifications.log')
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    notification_logger.addHandler(handler)


class LoggingNotifier(Notifier):
    """Notifier that writes messages to a log file."""
    
    def __init__(self, log_level: str = "INFO"):
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
    
    def send(self, message: str, recipient: str):
        """Log the notification message."""
        log_message = f"NOTIFICATION to {recipient}: {message}"
        notification_logger.log(self.log_level, log_message)
        
        # Also print to console for demo purposes
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"📝 [{timestamp}] Logged notification to {recipient}: {message}")


class ConsoleNotifier(Notifier):
    """Notifier that prints colorful messages to console."""
    
    def __init__(self, color: str = "blue"):
        self.colors = {
            "red": "\033[91m",
            "green": "\033[92m", 
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "purple": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
            "reset": "\033[0m"
        }
        self.color = self.colors.get(color, self.colors["blue"])
    
    def send(self, message: str, recipient: str):
        """Print a colorful notification to console."""
        reset = self.colors["reset"]
        print(
            f"{self.color}🔔 Console notification to {recipient}: "
            f"{message}{reset}"
        )
