from infrastructure.email_notifier import EmailNotifier, SMSNotifier
from infrastructure.txt_lead_repo import TxtFileLeadRepository
from services.lead_creator import LeadCreator


def main():
    # You can easily switch between repositories!
    # repo = InMemoryLeadRepository()  # In-memory storage
    repo = TxtFileLeadRepository("leads_data.txt")  # File-based storage
    
    creator = LeadCreator(
        repo=repo,
        notifiers=[EmailNotifier(), SMSNotifier()]
    )

    try:
        creator.create_lead("John Doe", "john@example.com")
        creator.create_lead("Jane Smith", "jane@example.com")
        print("Leads created successfully!")
        
        # Show all leads to demonstrate persistence
        all_leads = repo.find_all()
        print(f"\nTotal leads in repository: {len(all_leads)}")
        for lead in all_leads:
            print(f"  - {lead.name} ({lead.email}) [ID: {lead.id}]")
            
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
