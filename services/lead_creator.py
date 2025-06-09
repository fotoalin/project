import logging

from domain.lead import Lead

from .interfaces import LeadRepository

logger = logging.getLogger(__name__)


class LeadCreator:
    def __init__(self, repo: LeadRepository, notifiers):
        self.repo = repo
        # Handle both single notifier and list of notifiers
        if isinstance(notifiers, list):
            self.notifiers = notifiers
        else:
            self.notifiers = [notifiers]

    def create_lead(self, name: str, email: str) -> Lead:
        # Check for duplicate email
        existing_lead = self.repo.find_by_email(email)
        if existing_lead:
            raise ValueError(f"Lead with email {email} already exists")
        
        # Create lead without ID - let repository handle ID generation
        lead = Lead(name=name, email=email)
        
        # Repository assigns ID and returns the saved lead
        saved_lead = self.repo.save(lead)
        
        # Notify after successful save
        for notifier in self.notifiers:
            message = f"New lead created: {saved_lead.name}"
            notifier.send(message, saved_lead.email)
        
        log_msg = (
            f"Lead created successfully: {saved_lead.name} "
            f"with ID {saved_lead.id}"
        )
        logger.info(log_msg)
        return saved_lead
