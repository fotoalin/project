# services/tests/test_lead_creator.py
import pytest

from domain.lead import Lead
from services.lead_creator import LeadCreator


class FakeRepo:
    def __init__(self):
        self.saved = []

    def save(self, lead):
        # Assign ID if not present (like real repository would)
        if lead.id is None:
            lead.id = len(self.saved) + 1
        self.saved.append(lead)
        return lead  # Return the saved lead as per interface contract
    
    def find_by_email(self, email):
        """Find a lead by email address"""
        for lead in self.saved:
            if lead.email == email:
                return lead
        return None
    
    def find_all(self):
        """Return all saved leads"""
        return self.saved.copy()

class FakeNotifier:
    def __init__(self):
        self.messages = []

    def send(self, message, recipient):
        self.messages.append((message, recipient))


def test_create_lead_success():
    repo = FakeRepo()
    notifier = FakeNotifier()
    service = LeadCreator(repo, notifier)

    service.create_lead("Alin", "alin@example.com")

    assert len(repo.saved) == 1
    assert repo.saved[0].name == "Alin"
    assert repo.saved[0].email == "alin@example.com"
    assert len(notifier.messages) == 1
    assert notifier.messages[0][1] == "alin@example.com"


def test_create_lead_invalid_email():
    repo = FakeRepo()
    notifier = FakeNotifier()
    service = LeadCreator(repo, notifier)

    with pytest.raises(ValueError):
        service.create_lead("Alin", "no-at-symbol")

    assert repo.saved == []
    assert notifier.messages == []
