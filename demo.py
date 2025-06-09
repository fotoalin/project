#!/usr/bin/env python3
"""
Demo of SOLID principles in practice with Lead Management System.

This demonstrates:
- Single Responsibility: Each class has one clear purpose
- Open/Closed: Easy to add new storage/notification without changing existing code
- Liskov Substitution: Repository implementations are interchangeable
- Interface Segregation: Clean, focused interfaces
- Dependency Inversion: Services depend on abstractions, not implementations
"""

from infrastructure.db_lead_repo import InMemoryLeadRepository
from infrastructure.email_notifier import EmailNotifier, SMSNotifier
from infrastructure.txt_lead_repo import TxtFileLeadRepository
from services.lead_creator import LeadCreator


def demo_repository_switching():
    """Demonstrate how we can easily switch between different storage backends."""
    print("=== SOLID Principles Demo: Repository Pattern ===\n")
    
    # Demo 1: In-Memory Repository
    print("1. Using In-Memory Repository:")
    memory_repo = InMemoryLeadRepository()
    creator_memory = LeadCreator(
        repo=memory_repo,
        notifiers=[EmailNotifier()]
    )
    
    try:
        creator_memory.create_lead("Alice Johnson", "alice@example.com")
        creator_memory.create_lead("Bob Wilson", "bob@example.com")
        
        leads = memory_repo.find_all()
        print(f"   Leads in memory: {len(leads)}")
        for lead in leads:
            print(f"   - {lead.name} ({lead.email}) [ID: {lead.id}]")
    except ValueError as e:
        print(f"   Error: {e}")
    
    print()
    
    # Demo 2: File-Based Repository
    print("2. Using File-Based Repository:")
    file_repo = TxtFileLeadRepository("demo_leads.txt")
    creator_file = LeadCreator(
        repo=file_repo,
        notifiers=[EmailNotifier(), SMSNotifier()]
    )
    
    try:
        creator_file.create_lead("Charlie Brown", "charlie@example.com")
        creator_file.create_lead("Diana Prince", "diana@example.com")
        
        leads = file_repo.find_all()
        print(f"   Leads in file: {len(leads)}")
        for lead in leads:
            print(f"   - {lead.name} ({lead.email}) [ID: {lead.id}]")
    except ValueError as e:
        print(f"   Error: {e}")
    
    print()


def demo_duplicate_prevention():
    """Demonstrate duplicate email prevention."""
    print("=== Demo: Duplicate Prevention ===\n")
    
    repo = InMemoryLeadRepository()
    creator = LeadCreator(repo=repo, notifiers=[EmailNotifier()])
    
    try:
        # First lead should succeed
        creator.create_lead("John Doe", "john@test.com")
        print("✅ First lead created successfully")
        
        # Second lead with same email should fail
        creator.create_lead("John Smith", "john@test.com")
        print("❌ This should not print - duplicate should be prevented")
        
    except ValueError as e:
        print(f"✅ Duplicate prevented: {e}")
    
    print()


def demo_notification_flexibility():
    """Demonstrate flexible notification system."""
    print("=== Demo: Flexible Notification System ===\n")
    
    repo = InMemoryLeadRepository()
    
    # Single notifier
    print("1. Single Email Notifier:")
    creator1 = LeadCreator(repo=repo, notifiers=EmailNotifier())
    creator1.create_lead("Test User 1", "test1@example.com")
    
    print("\n2. Multiple Notifiers:")
    creator2 = LeadCreator(
        repo=repo, 
        notifiers=[EmailNotifier(), SMSNotifier()]
    )
    creator2.create_lead("Test User 2", "test2@example.com")
    
    print()


def demo_solid_principles():
    """Showcase how each SOLID principle is demonstrated."""
    print("=== SOLID Principles Demonstrated ===\n")
    
    print("🔹 Single Responsibility Principle:")
    print("   - Lead: Only holds lead data")
    print("   - LeadRepository: Only handles storage")
    print("   - Notifier: Only handles notifications")
    print("   - LeadCreator: Only orchestrates lead creation")
    
    print("\n🔹 Open/Closed Principle:")
    print("   - Easy to add new repository types (Database, API, etc.)")
    print("   - Easy to add new notifiers (Slack, WhatsApp, etc.)")
    print("   - No need to modify existing classes")
    
    print("\n🔹 Liskov Substitution Principle:")
    print("   - InMemoryLeadRepository and TxtFileLeadRepository")
    print("   - Can be used interchangeably")
    print("   - EmailNotifier and SMSNotifier are interchangeable")
    
    print("\n🔹 Interface Segregation Principle:")
    print("   - LeadRepository interface: focused on storage operations")
    print("   - Notifier interface: focused on sending messages")
    print("   - No client is forced to depend on unused methods")
    
    print("\n🔹 Dependency Inversion Principle:")
    print("   - LeadCreator depends on abstractions (interfaces)")
    print("   - Not on concrete implementations")
    print("   - Allows for easy testing and flexibility")
    
    print()


def main():
    """Run all demonstrations."""
    print("🚀 Lead Management System - SOLID Principles Demo\n")
    
    demo_solid_principles()
    demo_repository_switching()
    demo_duplicate_prevention()
    demo_notification_flexibility()
    
    print("✨ Demo completed! Check the generated files:")
    print("   - demo_leads.txt (file-based repository data)")


if __name__ == "__main__":
    main()
