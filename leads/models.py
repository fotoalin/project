# leads/models.py
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class LeadModel:
    name: str
    email: str
    id: Optional[int] = None
    
    def __post_init__(self):
        """Validate the lead data after initialization"""
        if not self.name or not self.name.strip():
            raise ValueError("Name cannot be empty")

        # Only validate ID if it's provided (not None)
        if self.id is not None:
            if not isinstance(self.id, int) or self.id < 1:
                raise ValueError("ID must be a positive integer")
        
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email format")
        
        if len(self.name) > 100:
            raise ValueError("Name cannot exceed 100 characters")
