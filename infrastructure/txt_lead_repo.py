# infrastructure/txt_lead_repo.py
import json
import logging
import os
from typing import List, Optional

from domain.models import Lead
from services.interfaces import LeadRepository

logger = logging.getLogger(__name__)


class TxtFileLeadRepository(LeadRepository):
    def __init__(self, file_path: str = "leads.txt"):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create the file if it doesn't exist"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                f.write("")  # Create empty file
    
    def _read_leads_from_file(self) -> List[Lead]:
        """Read all leads from the text file"""
        leads = []
        try:
            with open(self.file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:  # Skip empty lines
                        try:
                            lead_data = json.loads(line)
                            lead = Lead(
                                name=lead_data['name'],
                                email=lead_data['email'],
                                id=lead_data.get('id')
                            )
                            leads.append(lead)
                        except (json.JSONDecodeError, KeyError) as e:
                            logger.warning(
                                f"Skipping invalid line: {line}. Error: {e}"
                            )
        except FileNotFoundError:
            logger.info(
                f"File {self.file_path} not found, "
                f"starting with empty repository"
            )
        return leads
    
    def _write_leads_to_file(self, leads: List[Lead]):
        """Write all leads to the text file"""
        with open(self.file_path, 'w') as f:
            for lead in leads:
                lead_data = {
                    'name': lead.name,
                    'email': lead.email,
                    'id': lead.id
                }
                f.write(json.dumps(lead_data) + '\n')
    
    def _get_next_id(self, leads: List[Lead]) -> int:
        """Get the next available ID"""
        if not leads:
            return 1
        max_id = max(lead.id for lead in leads if lead.id is not None)
        return max_id + 1
    
    def save(self, lead: Lead) -> Lead:
        """Save a lead and return it with an assigned ID"""
        leads = self._read_leads_from_file()
        
        # Assign ID if not present
        if lead.id is None:
            lead.id = self._get_next_id(leads)
        
        # Check if lead already exists (update case)
        existing_index = None
        for i, existing_lead in enumerate(leads):
            if existing_lead.id == lead.id:
                existing_index = i
                break
        
        if existing_index is not None:
            leads[existing_index] = lead
        else:
            leads.append(lead)
        
        self._write_leads_to_file(leads)
        log_msg = (
            f"Saved lead to file: {lead.name} ({lead.email}) "
            f"with ID {lead.id}"
        )
        logger.info(log_msg)
        return lead
    
    def find_by_email(self, email: str) -> Optional[Lead]:
        """Find a lead by email address"""
        leads = self._read_leads_from_file()
        for lead in leads:
            if lead.email == email:
                return lead
        return None
    
    def find_all(self) -> List[Lead]:
        """Return all leads"""
        return self._read_leads_from_file()
