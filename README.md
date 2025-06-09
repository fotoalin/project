# Lead Management System - SOLID Principles Demo

A pure Python implementation of a lead management system that demonstrates all five SOLID principles through clean architecture, dependency injection, and multiple storage/notification strategies.

## 🎯 Project Overview

This project showcases a lead management system in pure Python while maintaining SOLID principles. It demonstrates:

- **Domain-driven design** with clean separation of concerns
- **Repository pattern** with interchangeable storage backends
- **Strategy pattern** for flexible notification systems
- **Dependency injection** for loose coupling
- **Interface segregation** with focused abstractions

## 🏗️ Architecture

```
project/
├── domain/           # Business entities and core logic
│   └── lead.py      # Lead dataclass with validation
├── services/        # Application services and interfaces
│   ├── interfaces.py      # Abstract base classes
│   └── lead_creator.py    # Business logic service
├── infrastructure/ # Implementation details
│   ├── db_lead_repo.py    # In-memory repository
│   ├── txt_lead_repo.py   # File-based repository
│   └── email_notifier.py  # Email and SMS notifiers
├── tests/          # Unit tests
└── demo.py         # SOLID principles demonstration
```

## 🎨 SOLID Principles Demonstrated

### 1. Single Responsibility Principle (SRP)
Each class has one clear responsibility:
- `Lead`: Holds lead data and validates it
- `LeadRepository`: Handles storage operations only
- `Notifier`: Sends messages only
- `LeadCreator`: Orchestrates lead creation workflow

### 2. Open/Closed Principle (OCP)
The system is open for extension but closed for modification:
- Add new repository types (Database, API, Cache) without changing existing code
- Add new notifiers (Slack, WhatsApp, Push) without modifying current implementations
- Extend notification strategies without touching the core service

### 3. Liskov Substitution Principle (LSP)
Implementations are perfectly interchangeable:
- `InMemoryLeadRepository` and `TxtFileLeadRepository` can be swapped seamlessly
- `EmailNotifier` and `SMSNotifier` are completely substitutable
- All implementations honor their interface contracts

### 4. Interface Segregation Principle (ISP)
Interfaces are focused and cohesive:
- `LeadRepository`: Only storage-related methods (`save`, `find_by_email`, `find_all`)
- `Notifier`: Only messaging-related methods (`send`)
- No client depends on methods it doesn't use

### 5. Dependency Inversion Principle (DIP)
High-level modules depend on abstractions:
- `LeadCreator` depends on `LeadRepository` and `Notifier` interfaces
- Not on concrete implementations
- Enables easy testing with mocks and flexible configuration

## 🚀 Quick Start

### Run the Demo

```bash
cd project
python3 demo.py
```

This will showcase:
- Repository pattern with different storage backends
- Duplicate email prevention
- Flexible notification systems
- All SOLID principles in action

### Run Tests

```bash
python3 -m pytest tests/ -v
```

### Run Simple Application

```bash
python3 app.py
```

## 💡 Key Features

### Repository Implementations

1. **In-Memory Repository** (`InMemoryLeadRepository`)
   - Fast, temporary storage
   - Perfect for testing and development
   - Data lost on application restart

2. **File-Based Repository** (`TxtFileLeadRepository`)
   - Persistent JSON Lines storage
   - Human-readable format
   - Suitable for small datasets

### Notification Systems

1. **Email Notifier** - Sends email notifications (mocked)
2. **SMS Notifier** - Sends SMS messages (mocked)

Both can be used individually or combined for multi-channel notifications.

### Business Features

- **Duplicate Prevention**: Prevents multiple leads with the same email
- **Automatic ID Assignment**: Repository handles unique ID generation
- **Data Validation**: Email format validation in the domain model
- **Comprehensive Logging**: Track all operations with structured logging

## 🔧 Code Examples

### Basic Usage

```python
from infrastructure.txt_lead_repo import TxtFileLeadRepository
from infrastructure.email_notifier import EmailNotifier
from services.lead_creator import LeadCreator

# Create service with file storage and email notifications
repo = TxtFileLeadRepository("leads.txt")
creator = LeadCreator(
    repo=repo,
    notifiers=[EmailNotifier()]
)

# Create a lead
try:
    lead = creator.create_lead("John Doe", "john@example.com")
    print(f"Created lead: {lead.name} [ID: {lead.id}]")
except ValueError as e:
    print(f"Error: {e}")
```

### Repository Switching

```python
# Switch between storage backends easily
from infrastructure.db_lead_repo import InMemoryLeadRepository

# Use in-memory storage instead
repo = InMemoryLeadRepository()
creator = LeadCreator(repo=repo, notifiers=[EmailNotifier()])
```

### Multiple Notifiers

```python
from infrastructure.email_notifier import EmailNotifier, SMSNotifier

# Send both email and SMS notifications
creator = LeadCreator(
    repo=repo,
    notifiers=[EmailNotifier(), SMSNotifier()]
)
```

### Custom Implementations

Extend the system by implementing the interfaces:

```python
from services.interfaces import LeadRepository, Notifier

class DatabaseLeadRepository(LeadRepository):
    def save(self, lead): 
        # Your database logic here
        pass
    
    def find_by_email(self, email):
        # Your query logic here
        pass
    
    def find_all(self):
        # Your retrieval logic here
        pass

class SlackNotifier(Notifier):
    def send(self, message, recipient):
        # Your Slack integration here
        pass
```

## 🧪 Testing

The project includes comprehensive unit tests with:
- **Fake implementations** for testing in isolation
- **Mock objects** to verify interactions
- **Test coverage** for all business logic
- **Error case validation**

### Test Structure

```python
class FakeRepo:
    """Test double that implements LeadRepository interface"""
    def save(self, lead): # ...
    def find_by_email(self, email): # ...
    def find_all(self): # ...

class FakeNotifier:
    """Test double for notification testing"""
    def send(self, message, recipient): # ...
```

## 📊 Benefits Achieved

### ✅ Maintainability
- Clear separation of concerns
- Single responsibility for each class
- Easy to understand and modify

### ✅ Extensibility  
- Add new storage backends without changing existing code
- Plug in new notification channels seamlessly
- Extend business logic without breaking existing features

### ✅ Testability
- Dependencies injected via constructor
- Easy to mock and unit test
- Fast test execution with fake implementations

### ✅ Flexibility
- Runtime configuration of storage and notifications
- Mix and match different implementations
- Easy to adapt to different deployment environments

### Pure Python
- Clean domain models with dataclasses
- Pure business logic in service layer
- Framework-independent core
- Pluggable infrastructure implementations

## 🎓 Learning Outcomes

By studying this codebase, you'll learn:
- How to apply SOLID principles in real-world scenarios
- Repository and Strategy pattern implementations
- Dependency injection without a framework
- Clean architecture principles
- Test-driven development practices
- Domain-driven design concepts

## 🛠️ Future Enhancements

The architecture supports easy addition of:
- Database repository (SQLite, PostgreSQL, etc.)
- API-based storage (REST, GraphQL)
- Advanced notifications (Slack, Discord, Push)
- Lead scoring and analytics
- Bulk operations and import/export
- Advanced validation rules
- Audit logging and event sourcing

---

*This project serves as a practical example of clean architecture and SOLID principles in Python. It's designed for educational purposes and as a foundation for building larger, more complex systems.*
