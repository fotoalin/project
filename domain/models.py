# domain/lead.py
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Lead:
    name: str
    email: str
    id: int = None

    def is_valid_email(self) -> bool:
        return "@" in self.email

    def is_valid_id(self) -> bool:
        return self.id is None or (isinstance(self.id, int) and self.id > 0)
    
    def __post_init__(self):
        """Validate the lead data after initialization"""
        if not self.name or not self.name.strip():
            raise ValueError("Name cannot be empty")

        # Only validate ID if it's provided (not None)
        if self.id is not None and not self.is_valid_id():
            raise ValueError("ID must be a positive integer greater than 0")

        if not self.is_valid_email():
            raise ValueError("Invalid email format")

        if len(self.name) > 100:
            raise ValueError("Name cannot exceed 100 characters")