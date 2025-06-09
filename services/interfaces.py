# services/interfaces.py
import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models import Lead

logger = logging.getLogger(__name__)


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str, recipient: str) -> None:
        pass


class LeadRepository(ABC):
    @abstractmethod
    def save(self, lead: Lead) -> Lead:
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Lead]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[Lead]:
        pass
