"""
JSON Repository Implementation - demonstrates Open/Closed Principle

This shows how easy it is to add a new storage backend without modifying
existing code. The JSON repository stores all leads in a single JSON file
with better structure than the line-by-line text format.
"""
import json
import logging
import os
from typing import List, Optional

from domain.models import Lead
from services.interfaces import LeadRepository

logger = logging.getLogger(__name__)


class JsonLeadRepository(LeadRepository):
    """Repository that stores leads in a structured JSON file."""
    
    def __init__(self, file_path: str = "leads.json"):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create an empty JSON file if it doesn't exist."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({"leads": [], "next_id": 1}, f, indent=2)
    
    def _read_data(self) -> dict:
        """Read the entire JSON structure from file."""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Error reading {self.file_path}: {e}")
            return {"leads": [], "next_id": 1}
    
    def _write_data(self, data: dict):
        """Write the entire JSON structure to file."""
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _leads_from_data(self, data: dict) -> List[Lead]:
        """Convert JSON data to Lead objects."""
        leads = []
        for lead_data in data.get("leads", []):
            try:
                lead = Lead(
                    name=lead_data['name'],
                    email=lead_data['email'],
                    id=lead_data.get('id')
                )
                leads.append(lead)
            except KeyError as e:
                logger.warning(f"Invalid lead data: {lead_data}. Error: {e}")
        return leads
    
    def save(self, lead: Lead) -> Lead:
        """Save a lead and return it with an assigned ID."""
        data = self._read_data()
        
        # Assign ID if not present
        if lead.id is None:
            lead.id = data.get("next_id", 1)
            data["next_id"] = lead.id + 1
        
        # Convert lead to dict
        lead_dict = {
            "id": lead.id,
            "name": lead.name,
            "email": lead.email
        }
        
        # Check if lead already exists (update case)
        leads = data.get("leads", [])
        existing_index = None
        for i, existing_lead in enumerate(leads):
            if existing_lead.get("id") == lead.id:
                existing_index = i
                break
        
        if existing_index is not None:
            leads[existing_index] = lead_dict
        else:
            leads.append(lead_dict)
        
        data["leads"] = leads
        self._write_data(data)
        
        logger.info(
            f"Saved lead to JSON: {lead.name} ({lead.email}) "
            f"with ID {lead.id}"
        )
        return lead
    
    def find_by_email(self, email: str) -> Optional[Lead]:
        """Find a lead by email address."""
        data = self._read_data()
        leads = self._leads_from_data(data)
        
        for lead in leads:
            if lead.email == email:
                return lead
        return None
    
    def find_all(self) -> List[Lead]:
        """Return all leads."""
        data = self._read_data()
        return self._leads_from_data(data)
