"""
Comprehensive unit tests for all repository and notifier implementations.

This test suite validates that all implementations correctly follow their
interfaces and can be used interchangeably (Liskov Substitution Principle).
"""
import json
import os
import tempfile
from unittest.mock import patch

import pytest

from domain.lead import Lead
from infrastructure.db_lead_repo import InMemoryLeadRepository
from infrastructure.email_notifier import EmailNotifier, SMSNotifier
from infrastructure.json_lead_repo import JsonLeadRepository
from infrastructure.logging_notifier import ConsoleNotifier, LoggingNotifier
from infrastructure.txt_lead_repo import TxtFileLeadRepository
from services.lead_creator import LeadCreator


class TestRepositoryImplementations:
    """Test all repository implementations for interface compliance."""

    @pytest.fixture(params=[
        InMemoryLeadRepository,
        lambda: TxtFileLeadRepository(tempfile.mktemp(suffix='.txt')),
        lambda: JsonLeadRepository(tempfile.mktemp(suffix='.json'))
    ])
    def repository(self, request):
        """Parameterized fixture that tests all repository types."""
        if callable(request.param):
            repo = request.param()
        else:
            repo = request.param()
        
        yield repo
        
        # Cleanup file-based repositories
        if hasattr(repo, 'file_path') and os.path.exists(repo.file_path):
            os.unlink(repo.file_path)

    def test_save_assigns_id_to_new_lead(self, repository):
        """Test that save() assigns an ID to leads without one."""
        lead = Lead(name="Test User", email="test@example.com")
        assert lead.id is None
        
        saved_lead = repository.save(lead)
        
        assert saved_lead.id is not None
        assert saved_lead.id >= 1
        assert saved_lead.name == "Test User"
        assert saved_lead.email == "test@example.com"

    def test_save_preserves_existing_id(self, repository):
        """Test that save() preserves existing IDs."""
        lead = Lead(name="Test User", email="test@example.com", id=42)
        
        saved_lead = repository.save(lead)
        
        assert saved_lead.id == 42

    def test_find_by_email_returns_correct_lead(self, repository):
        """Test that find_by_email() returns the correct lead."""
        lead1 = Lead(name="User 1", email="user1@example.com")
        lead2 = Lead(name="User 2", email="user2@example.com")
        
        repository.save(lead1)
        repository.save(lead2)
        
        found = repository.find_by_email("user1@example.com")
        
        assert found is not None
        assert found.name == "User 1"
        assert found.email == "user1@example.com"

    def test_find_by_email_returns_none_for_missing(self, repository):
        """Test that find_by_email() returns None for non-existent emails."""
        found = repository.find_by_email("nonexistent@example.com")
        assert found is None

    def test_find_all_returns_all_leads(self, repository):
        """Test that find_all() returns all saved leads."""
        leads = [
            Lead(name="User 1", email="user1@example.com"),
            Lead(name="User 2", email="user2@example.com"),
            Lead(name="User 3", email="user3@example.com")
        ]
        
        for lead in leads:
            repository.save(lead)
        
        all_leads = repository.find_all()
        
        assert len(all_leads) == 3
        emails = [lead.email for lead in all_leads]
        assert "user1@example.com" in emails
        assert "user2@example.com" in emails
        assert "user3@example.com" in emails

    def test_sequential_ids(self, repository):
        """Test that IDs are assigned sequentially."""
        lead1 = repository.save(Lead(name="User 1", email="user1@example.com"))
        lead2 = repository.save(Lead(name="User 2", email="user2@example.com"))
        
        assert lead2.id == lead1.id + 1


class TestNotifierImplementations:
    """Test all notifier implementations for interface compliance."""

    def test_email_notifier_sends_message(self):
        """Test EmailNotifier sends messages correctly."""
        notifier = EmailNotifier()
        
        with patch('infrastructure.email_notifier.send_mail') as mock_send:
            notifier.send("Test message", "test@example.com")
            
            mock_send.assert_called_once_with(
                "Lead Notification",
                "Test message", 
                "noreply@example.com",
                ["test@example.com"]
            )

    def test_sms_notifier_sends_message(self):
        """Test SMSNotifier sends messages correctly."""
        notifier = SMSNotifier()
        
        with patch('infrastructure.email_notifier.send_sms') as mock_send:
            notifier.send("Test message", "test@example.com")
            
            mock_send.assert_called_once_with(
                "Test message",
                "test@example.com"
            )

    def test_console_notifier_prints_message(self, capsys):
        """Test ConsoleNotifier prints colorful messages."""
        notifier = ConsoleNotifier("red")
        
        notifier.send("Test message", "test@example.com")
        
        captured = capsys.readouterr()
        assert "Console notification to test@example.com" in captured.out
        assert "Test message" in captured.out
        assert "\033[91m" in captured.out  # Red color code

    def test_logging_notifier_logs_message(self, caplog):
        """Test LoggingNotifier writes to log."""
        notifier = LoggingNotifier()
        
        with caplog.at_level("INFO", logger="notifications"):
            notifier.send("Test message", "test@example.com")
        
        assert len(caplog.records) == 1
        assert "NOTIFICATION to test@example.com: Test message" in caplog.records[0].getMessage()


class TestIntegrationScenarios:
    """Test complete scenarios with different combinations."""

    def test_repository_interchangeability(self):
        """Test that repositories can be swapped without code changes."""
        # Test with different repositories
        repositories = [
            InMemoryLeadRepository(),
            TxtFileLeadRepository(tempfile.mktemp(suffix='.txt')),
            JsonLeadRepository(tempfile.mktemp(suffix='.json'))
        ]
        
        for repo in repositories:
            creator = LeadCreator(repo=repo, notifiers=[])
            
            # Same operations should work with all repositories
            lead = creator.create_lead("Test User", "test@repo.com")
            assert lead.id is not None
            
            found = repo.find_by_email("test@repo.com")
            assert found is not None
            assert found.name == "Test User"
            
            # Cleanup
            if hasattr(repo, 'file_path') and os.path.exists(repo.file_path):
                os.unlink(repo.file_path)

    def test_notifier_combinations(self):
        """Test various notifier combinations."""
        repo = InMemoryLeadRepository()
        
        # Single notifier
        creator1 = LeadCreator(repo=repo, notifiers=EmailNotifier())
        creator1.create_lead("User 1", "user1@example.com")
        
        # Multiple notifiers
        creator2 = LeadCreator(
            repo=repo, 
            notifiers=[EmailNotifier(), SMSNotifier(), ConsoleNotifier()]
        )
        creator2.create_lead("User 2", "user2@example.com")
        
        # Verify both leads were created
        all_leads = repo.find_all()
        assert len(all_leads) == 2

    def test_duplicate_prevention_across_repositories(self):
        """Test duplicate prevention works with all repository types."""
        for repo_class in [InMemoryLeadRepository, 
                          lambda: TxtFileLeadRepository(tempfile.mktemp(suffix='.txt')),
                          lambda: JsonLeadRepository(tempfile.mktemp(suffix='.json'))]:
            
            if callable(repo_class):
                repo = repo_class()
            else:
                repo = repo_class()
            
            creator = LeadCreator(repo=repo, notifiers=[])
            
            # First lead should succeed
            creator.create_lead("Test User", "duplicate@test.com")
            
            # Second lead with same email should fail
            with pytest.raises(ValueError, match="already exists"):
                creator.create_lead("Another User", "duplicate@test.com")
            
            # Cleanup
            if hasattr(repo, 'file_path') and os.path.exists(repo.file_path):
                os.unlink(repo.file_path)


class TestFileFormats:
    """Test file format specifics for file-based repositories."""

    def test_txt_repository_format(self):
        """Test that TxtFileLeadRepository uses JSON lines format."""
        temp_file = tempfile.mktemp(suffix='.txt')
        repo = TxtFileLeadRepository(temp_file)
        
        repo.save(Lead(name="Test User", email="test@example.com"))
        
        with open(temp_file, 'r') as f:
            line = f.readline().strip()
            data = json.loads(line)
            assert data['name'] == "Test User"
            assert data['email'] == "test@example.com"
            assert 'id' in data
        
        os.unlink(temp_file)

    def test_json_repository_format(self):
        """Test that JsonLeadRepository uses structured JSON format."""
        temp_file = tempfile.mktemp(suffix='.json')
        repo = JsonLeadRepository(temp_file)
        
        repo.save(Lead(name="Test User", email="test@example.com"))
        
        with open(temp_file, 'r') as f:
            data = json.load(f)
            assert 'leads' in data
            assert 'next_id' in data
            assert len(data['leads']) == 1
            assert data['leads'][0]['name'] == "Test User"
        
        os.unlink(temp_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
