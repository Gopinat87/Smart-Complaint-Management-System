# SmartComplain — Complaint Management System
## Stack: Python · Django · MySQL/SQLite · HTML · CSS · JS

---

## Quick Start

```bash
# 1. Clone / extract project
cd complaint_system

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure database
# For SQLite (default, no setup needed) — skip to step 5
# For MySQL:
#   - Create DB: CREATE DATABASE complaint_db;
#   - Edit complaint_project/settings.py → uncomment DATABASES MySQL block

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Seed categories
python manage.py seed_categories

# 7. Create admin user
python manage.py createsuperuser

# 8. Run server
python manage.py runserver
```

Open: http://127.0.0.1:8000

---

## Features
- User register / login / logout
- Submit complaints with category, priority, location, photo
- Track complaint status (Pending → Investigating → Resolved)
- Admin dashboard with stats and category breakdown
- Admin can update status + add notes
- Real-time notifications for both users and admins
- Fully responsive dark UI

## Project Structure
```
complaint_system/
├── manage.py
├── requirements.txt
├── complaint_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── complaint_app/
    ├── models.py          # Complaint, Category, Update, Notification
    ├── views.py           # All views (auth, user, admin)
    ├── forms.py           # Register, Login, Complaint, UpdateStatus
    ├── urls.py            # All URL patterns
    ├── admin.py           # Django admin registration
    ├── management/commands/seed_categories.py
    ├── templates/complaint_app/
    │   ├── base.html
    │   ├── login.html
    │   ├── register.html
    │   ├── dashboard.html
    │   ├── submit_complaint.html
    │   ├── my_complaints.html
    │   ├── complaint_detail.html
    │   ├── admin_dashboard.html
    │   ├── admin_complaints.html
    │   ├── admin_complaint_detail.html
    │   ├── admin_users.html
    │   └── notifications.html
    └── static/complaint_app/
        ├── css/style.css
        └── js/main.js
```

## Default Categories (seeded)
💧 Water Supply · ⚡ Electricity · 🗑️ Sanitation · 🛣️ Roads
🔒 Security · 📶 Internet/Wi-Fi · 🔊 Noise · 🔧 Maintenance
🐛 Pest Control · 📋 Other
