# infrastructure/db_lead_repo.py
import logging

from domain.models import Lead
from services.interfaces import LeadRepository

logger = logging.getLogger(__name__)


class InMemoryLeadRepository(LeadRepository):
    def __init__(self):
        self._leads = []
        self._next_id = 1
    
    def save(self, lead):
        """Save a lead and return it with an assigned ID"""
        if lead.id is None:
            lead.id = self._next_id
            self._next_id += 1
        
        # Check if lead already exists (update case)
        existing_index = None
        for i, existing_lead in enumerate(self._leads):
            if existing_lead.id == lead.id:
                existing_index = i
                break
        
        if existing_index is not None:
            self._leads[existing_index] = lead
        else:
            self._leads.append(lead)
        
        log_msg = f"Saved lead: {lead.name} ({lead.email}) with ID {lead.id}"
        logger.info(log_msg)
        return lead
    
    def find_by_email(self, email):
        """Find a lead by email address"""
        for lead in self._leads:
            if lead.email == email:
                return lead
        return None
    
    def find_all(self):
        """Return all leads"""
        return self._leads.copy()
