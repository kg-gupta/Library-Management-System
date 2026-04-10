# Library Management System

## 📖 Overview
A Django-based system for managing books, users, and borrowing transactions.

## ✨ Features
- User authentication
- Book management
- Borrow and return functionality
- Notifications

## 🛠️ Technology Stack
- Python
- Django
- SQLite
- HTML/CSS/Bootstrap
## 📂 Project Structure

Library_Management_System/
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/
│   │   └── accounts/
│   │       ├── login.html
│   │       ├── register.html
│   │       └── profile.html
│   └── static/
│       └── accounts/
│           ├── css/
│           └── js/
│
├── books/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/
│   │   └── books/
│   │       ├── book_list.html
│   │       ├── book_detail.html
│   │       └── book_form.html
│   └── static/
│       └── books/
│           ├── css/
│           └── js/
│
├── transactions/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/
│   │   └── transactions/
│   │       ├── issue_book.html
│   │       ├── return_book.html
│   │       └── transaction_list.html
│   └── services/
│       └── transaction_service.py
│
├── notifications/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│       └── notifications/
│           └── notification_list.html
│
├── templates/
│   └── base.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── manage.py
└── db.sqlite3
## 📊 Diagrams

### 1. Entity Relationship (ER) Diagram
![ER Diagram](docs/er_diagram.png)

### 2. UML Class Diagram
![UML Diagram](docs/uml_class_diagram.png)

### 3. System Flowchart
![Flowchart](docs/flowchart.png)

## 🧩 Main Classes

- **User** – Handles authentication and user details.
- **Book** – Stores information about books.
- **Transaction** – Manages borrowing and returning of books.
- **Notification** – Sends alerts to users.

## 🔗 Relationships

- A **User** can have multiple **Transactions** (1:N).
- A **Book** can be associated with multiple **Transactions** (1:N).
- A **User** can receive multiple **Notifications** (1:N).
- Each **Transaction** links one **User** and one **Book**.
## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd library-management-system
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Linux/Mac
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
    
---

### **Step 8: Add Author and License**

```markdown
## 👨‍💻 Author
Kartik Gupta

## 📄 License
This project is developed for academic purposes.