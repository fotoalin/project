#!/usr/bin/env python3
"""
Advanced SOLID Principles Demo - Extension Showcase

This demo shows how the Open/Closed Principle allows us to easily extend
the system with new repository and notifier implementations without
modifying any existing code.
"""

from infrastructure.db_lead_repo import InMemoryLeadRepository
from infrastructure.email_notifier import EmailNotifier, SMSNotifier
from infrastructure.json_lead_repo import JsonLeadRepository
from infrastructure.logging_notifier import ConsoleNotifier, LoggingNotifier
from infrastructure.txt_lead_repo import TxtFileLeadRepository
from services.lead_creator import LeadCreator


def demo_multiple_repositories():
    """Demonstrate different repository implementations."""
    print("=== Repository Implementations Showcase ===\n")
    
    repositories = [
        ("In-Memory Repository", InMemoryLeadRepository()),
        ("Text File Repository", TxtFileLeadRepository("advanced_demo.txt")),
        ("JSON Repository", JsonLeadRepository("advanced_demo.json"))
    ]
    
    for name, repo in repositories:
        print(f"📊 Testing {name}:")
        creator = LeadCreator(repo=repo, notifiers=[ConsoleNotifier("green")])
        
        try:
            # Create some test leads
            creator.create_lead("Alice Smith", f"alice@{name.lower().replace(' ', '')}.com")
            creator.create_lead("Bob Jones", f"bob@{name.lower().replace(' ', '')}.com")
            
            # Show stored leads
            leads = repo.find_all()
            print(f"   📈 Stored {len(leads)} leads successfully")
            
            # Test find_by_email
            found = repo.find_by_email(f"alice@{name.lower().replace(' ', '')}.com")
            if found:
                print(f"   🔍 Found lead: {found.name} [ID: {found.id}]")
            
        except ValueError as e:
            print(f"   ❌ Error: {e}")
        
        print()


def demo_notification_matrix():
    """Demonstrate all notifier combinations."""
    print("=== Notification System Matrix ===\n")
    
    repo = InMemoryLeadRepository()
    
    notification_configs = [
        ("Single Email", [EmailNotifier()]),
        ("Single SMS", [SMSNotifier()]),
        ("Single Console", [ConsoleNotifier("purple")]),
        ("Single Logging", [LoggingNotifier()]),
        ("Email + SMS", [EmailNotifier(), SMSNotifier()]),
        ("All Channels", [
            EmailNotifier(), 
            SMSNotifier(), 
            ConsoleNotifier("yellow"),
            LoggingNotifier()
        ])
    ]
    
    for config_name, notifiers in notification_configs:
        print(f"📢 Testing {config_name}:")
        creator = LeadCreator(repo=repo, notifiers=notifiers)
        
        try:
            email = f"test@{config_name.lower().replace(' ', '').replace('+', 'and')}.com"
            creator.create_lead(f"Test User ({config_name})", email)
            print(f"   ✅ Notification sent via {len(notifiers)} channel(s)")
        except ValueError as e:
            print(f"   ❌ Error: {e}")
        
        print()


def demo_extensibility_showcase():
    """Show how easy it is to extend the system."""
    print("=== Extensibility Showcase ===\n")
    
    print("🔧 The system easily supports new implementations:")
    print("   ✅ Added JsonLeadRepository without changing existing code")
    print("   ✅ Added LoggingNotifier without modifying services")
    print("   ✅ Added ConsoleNotifier with color support")
    print("   ✅ All implementations are drop-in replacements")
    
    print("\n🎯 Future extensions could include:")
    print("   📊 DatabaseRepository (SQLite, PostgreSQL)")
    print("   🌐 APIRepository (REST, GraphQL endpoints)")
    print("   📱 SlackNotifier, DiscordNotifier")
    print("   🔔 PushNotifier, WebhookNotifier")
    print("   📈 AnalyticsRepository with metrics")
    
    print("\n💡 All following SOLID principles:")
    print("   🔹 Single Responsibility: Each class has one purpose")
    print("   🔹 Open/Closed: Open for extension, closed for modification")
    print("   🔹 Liskov Substitution: Perfect interchangeability")
    print("   🔹 Interface Segregation: Focused, cohesive interfaces")
    print("   🔹 Dependency Inversion: Depend on abstractions")
    
    print()


def demo_persistence_comparison():
    """Compare different persistence strategies."""
    print("=== Persistence Strategy Comparison ===\n")
    
    # Create same data in different repositories
    test_leads = [
        ("Engineering Lead", "engineering@company.com"),
        ("Sales Lead", "sales@company.com"),
        ("Marketing Lead", "marketing@company.com")
    ]
    
    repos = {
        "Memory": InMemoryLeadRepository(),
        "Text": TxtFileLeadRepository("comparison.txt"),
        "JSON": JsonLeadRepository("comparison.json")
    }
    
    # Populate all repositories
    for repo_name, repo in repos.items():
        creator = LeadCreator(repo=repo, notifiers=[])
        for name, email in test_leads:
            try:
                creator.create_lead(name, email)
            except ValueError:
                pass  # Skip duplicates
    
    # Compare the results
    for repo_name, repo in repos.items():
        leads = repo.find_all()
        print(f"📊 {repo_name} Repository: {len(leads)} leads stored")
        for lead in leads:
            print(f"   - {lead.name} ({lead.email}) [ID: {lead.id}]")
        print()
    
    print("📁 Check the generated files:")
    print("   - comparison.txt (line-by-line JSON)")
    print("   - comparison.json (structured JSON)")
    print("   - notifications.log (log file notifications)")
    print()


def main():
    """Run all advanced demonstrations."""
    print("🚀 Advanced SOLID Principles Demo\n")
    
    demo_extensibility_showcase()
    demo_multiple_repositories()
    demo_notification_matrix()
    demo_persistence_comparison()
    
    print("✨ Advanced demo completed!")
    print("   This showcases the power of SOLID principles for building")
    print("   extensible, maintainable, and testable systems.")


if __name__ == "__main__":
    main()
