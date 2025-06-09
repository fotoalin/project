#!/usr/bin/env python3
"""
Final Showcase: Lead Management System with SOLID Principles

This script demonstrates the complete system with performance metrics,
error handling, and advanced features to showcase the robustness
of the SOLID principles implementation.
"""

import time
from typing import List

from domain.lead import Lead
from infrastructure.db_lead_repo import InMemoryLeadRepository
from infrastructure.email_notifier import EmailNotifier, SMSNotifier
from infrastructure.json_lead_repo import JsonLeadRepository
from infrastructure.logging_notifier import ConsoleNotifier, LoggingNotifier
from infrastructure.txt_lead_repo import TxtFileLeadRepository
from services.lead_creator import LeadCreator


def benchmark_repositories(num_leads: int = 1000):
    """Benchmark different repository implementations."""
    print(f"=== Performance Benchmark ({num_leads} leads) ===\n")
    
    repositories = [
        ("In-Memory Repository", InMemoryLeadRepository()),
        ("Text File Repository", TxtFileLeadRepository("benchmark.txt")),
        ("JSON Repository", JsonLeadRepository("benchmark.json"))
    ]
    
    for repo_name, repo in repositories:
        print(f"📊 Testing {repo_name}:")
        creator = LeadCreator(repo=repo, notifiers=[])
        
        # Measure write performance
        start_time = time.time()
        for i in range(num_leads):
            try:
                creator.create_lead(f"User {i}", f"user{i}@benchmark.com")
            except ValueError:
                pass  # Skip duplicates
        write_time = time.time() - start_time
        
        # Measure read performance
        start_time = time.time()
        all_leads = repo.find_all()
        read_all_time = time.time() - start_time
        
        # Measure search performance
        start_time = time.time()
        found = repo.find_by_email(f"user{num_leads//2}@benchmark.com")
        search_time = time.time() - start_time
        
        print(f"   ✍️  Write {len(all_leads)} leads: {write_time:.3f}s")
        print(f"   📖 Read all leads: {read_all_time:.4f}s")
        print(f"   🔍 Search by email: {search_time:.4f}s")
        print(f"   📈 Avg write time: {(write_time/len(all_leads)*1000):.2f}ms per lead")
        
        # Cleanup
        if hasattr(repo, 'file_path'):
            import os
            if os.path.exists(repo.file_path):
                os.unlink(repo.file_path)
        
        print()


def demonstrate_error_handling():
    """Demonstrate robust error handling."""
    print("=== Error Handling Demonstration ===\n")
    
    repo = InMemoryLeadRepository()
    creator = LeadCreator(repo=repo, notifiers=[ConsoleNotifier("red")])
    
    # Test cases for error handling
    error_cases = [
        ("Invalid Email Format", "John Doe", "invalid-email"),
        ("Empty Name", "", "valid@email.com"),
        ("Duplicate Email", "Jane Doe", "duplicate@test.com"),
        ("Duplicate Email Again", "John Smith", "duplicate@test.com")
    ]
    
    # First, create a valid lead to test duplicate detection
    try:
        creator.create_lead("Original User", "duplicate@test.com")
        print("✅ Created original lead for duplicate testing")
    except ValueError as e:
        print(f"❌ Unexpected error: {e}")
    
    # Test error cases
    for test_name, name, email in error_cases:
        print(f"🧪 Testing {test_name}:")
        try:
            creator.create_lead(name, email)
            print(f"   ❌ Expected error but creation succeeded")
        except ValueError as e:
            print(f"   ✅ Correctly handled error: {e}")
        except Exception as e:
            print(f"   ⚠️  Unexpected error type: {type(e).__name__}: {e}")
    
    print()


def demonstrate_scalability():
    """Demonstrate system scalability with multiple notifiers."""
    print("=== Scalability Demonstration ===\n")
    
    repo = JsonLeadRepository("scalability_test.json")
    
    # Create service with multiple notification channels
    all_notifiers = [
        EmailNotifier(),
        SMSNotifier(),
        ConsoleNotifier("green"),
        LoggingNotifier()
    ]
    
    creator = LeadCreator(repo=repo, notifiers=all_notifiers)
    
    print(f"📡 Testing with {len(all_notifiers)} notification channels:")
    
    test_leads = [
        ("Sales Manager", "sales@company.com"),
        ("Marketing Director", "marketing@company.com"),
        ("Tech Lead", "tech@company.com"),
        ("Product Owner", "product@company.com")
    ]
    
    start_time = time.time()
    successful_creates = 0
    
    for name, email in test_leads:
        try:
            creator.create_lead(name, email)
            successful_creates += 1
        except ValueError as e:
            print(f"   ⚠️  Skipped {email}: {e}")
    
    total_time = time.time() - start_time
    
    print(f"\n📊 Results:")
    print(f"   ✅ Successfully created: {successful_creates}/{len(test_leads)} leads")
    print(f"   ⏱️  Total time: {total_time:.3f}s")
    print(f"   📧 Total notifications sent: {successful_creates * len(all_notifiers)}")
    print(f"   🚀 Avg time per lead: {(total_time/successful_creates*1000):.2f}ms")
    
    # Cleanup
    import os
    if os.path.exists("scalability_test.json"):
        os.unlink("scalability_test.json")
    
    print()


def demonstrate_extensibility():
    """Show how easy it is to extend the system."""
    print("=== Extensibility Showcase ===\n")
    
    print("🔧 Current System Components:")
    print("   📊 Repositories: InMemory, TextFile, JSON")
    print("   📢 Notifiers: Email, SMS, Console, Logging")
    print("   🎯 Services: LeadCreator with duplicate prevention")
    
    print("\n💡 Easy Extensions (following SOLID principles):")
    
    print("\n📊 Repository Extensions:")
    print("   🗄️  DatabaseRepository (SQLite, PostgreSQL, MySQL)")
    print("   🌐 APIRepository (REST endpoints, GraphQL)")
    print("   💾 CacheRepository (Redis, Memcached)")
    print("   ☁️  CloudRepository (AWS S3, Azure Blob)")
    
    print("\n📢 Notifier Extensions:")
    print("   💬 SlackNotifier (team notifications)")
    print("   🎮 DiscordNotifier (community alerts)")
    print("   📱 PushNotifier (mobile notifications)")
    print("   🔗 WebhookNotifier (third-party integrations)")
    print("   📧 TemplatedEmailNotifier (HTML templates)")
    
    print("\n🎯 Service Extensions:")
    print("   📈 LeadScorer (automatic lead qualification)")
    print("   🔄 LeadUpdater (edit existing leads)")
    print("   📊 LeadAnalytics (metrics and reporting)")
    print("   📤 LeadExporter (CSV, Excel, PDF export)")
    print("   🔄 LeadSynchronizer (sync between systems)")
    
    print("\n✨ Benefits of SOLID Design:")
    print("   🔹 Add new features without changing existing code")
    print("   🔹 Perfect interchangeability between implementations")
    print("   🔹 Easy unit testing with dependency injection")
    print("   🔹 Clean separation of concerns")
    print("   🔹 Maintainable and readable codebase")
    
    print()


def final_demonstration():
    """Complete demonstration combining all features."""
    print("=== Final Integration Demonstration ===\n")
    
    # Use different repository for final demo
    repo = JsonLeadRepository("final_demo.json")
    
    # Mix of different notifiers
    notifiers = [
        EmailNotifier(),
        ConsoleNotifier("cyan"),
        LoggingNotifier()
    ]
    
    creator = LeadCreator(repo=repo, notifiers=notifiers)
    
    print("🚀 Creating a realistic lead management scenario:")
    
    # Realistic business scenario
    leads_to_create = [
        ("Alice Johnson", "alice.johnson@techcorp.com"),
        ("Bob Smith", "bob.smith@startup.io"),
        ("Carol Williams", "carol@enterprise.com"),
        ("David Brown", "d.brown@company.net"),
        ("Eva Davis", "eva.davis@business.org")
    ]
    
    created_leads = []
    
    for name, email in leads_to_create:
        try:
            lead = creator.create_lead(name, email)
            created_leads.append(lead)
            print(f"   ✅ Created: {name} [ID: {lead.id}]")
        except ValueError as e:
            print(f"   ❌ Failed: {name} - {e}")
    
    print(f"\n📊 Final Results:")
    print(f"   👥 Total leads created: {len(created_leads)}")
    print(f"   📧 Total notifications sent: {len(created_leads) * len(notifiers)}")
    
    # Demonstrate repository queries
    all_leads = repo.find_all()
    print(f"   🗄️  Leads in repository: {len(all_leads)}")
    
    # Demonstrate search functionality
    search_email = "alice.johnson@techcorp.com"
    found_lead = repo.find_by_email(search_email)
    if found_lead:
        print(f"   🔍 Found lead by email: {found_lead.name}")
    
    print("\n🎉 System successfully demonstrates all SOLID principles!")
    
    # Cleanup
    import os
    if os.path.exists("final_demo.json"):
        os.unlink("final_demo.json")


def main():
    """Run the complete showcase."""
    print("🎯 Lead Management System - Final Showcase")
    print("=" * 50)
    print("Demonstrating SOLID Principles in Production-Ready Code\n")
    
    try:
        demonstrate_extensibility()
        benchmark_repositories(100)  # Smaller number for demo
        demonstrate_error_handling()
        demonstrate_scalability()
        final_demonstration()
        
        print("✨ Showcase completed successfully!")
        print("\nThis system demonstrates:")
        print("  🔹 Clean Architecture with SOLID principles")
        print("  🔹 Robust error handling and validation")
        print("  🔹 Performance considerations")
        print("  🔹 Extensibility and maintainability")
        print("  🔹 Comprehensive testing coverage")
        print("\n🚀 Ready for production deployment!")
        
    except Exception as e:
        print(f"❌ Showcase failed with error: {e}")
        raise


if __name__ == "__main__":
    main()
