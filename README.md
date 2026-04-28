# 🚀 Smart Complaint Management System

## 📌 Overview

The **Smart Complaint Management System** is a web-based application developed using **Django**. It enables users to submit, track, and manage complaints efficiently, while providing administrators with tools to monitor and resolve issues through a centralized dashboard.

This system is designed to streamline complaint handling processes in environments such as **colleges, hostels, and organizations**.

---

## ✨ Features

* 🔐 User Authentication (Login / Register / Logout)
* 📝 Submit Complaints with Category & Priority
* 📊 Dashboard for Tracking Complaints
* 🛠️ Admin Panel for Complaint Management
* 🔔 Notification System
* 📎 File/Image Upload Support
* 📂 Category-based Complaint Organization
* 📱 Responsive and Clean UI

---

## 🛠️ Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite
* **Version Control:** Git & GitHub

---

## 📁 Project Structure

```
complaint_system/
│── complaint_app/
│── complaint_project/
│── templates/
│── static/
│── db.sqlite3
│── manage.py
│── requirements.txt
```

---

## ⚙️ Installation & Setup Guide

Follow these steps to run the project locally:

---

### 🔥 Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

---

### 🔥 Step 2: Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

👉 Windows:

```bash
venv\Scripts\activate
```

👉 Mac/Linux:

```bash
source venv/bin/activate
```

---

### 🔥 Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 🔥 Step 4: Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 🔥 Step 5: Create Superuser

```bash
python manage.py createsuperuser
```

Enter:

* Username
* Email
* Password

---

### 🔥 Step 6: Run the Server 🚀

```bash
python manage.py runserver
```

---

### 🌐 Step 7: Open in Browser

* Home: http://127.0.0.1:8000/
* Admin Panel: http://127.0.0.1:8000/admin/

---

## 🧪 Usage

1. Register or login as a user
2. Submit a complaint with category and description
3. Track complaint status via dashboard
4. Admin can manage complaints from admin panel

---

## ⚠️ Important Notes

* Do not upload `venv/` and `db.sqlite3` to GitHub
* Add them to `.gitignore`
* Ensure migrations are applied before running

---

## 📌 Future Enhancements

* Email Notifications
* Real-time Updates (WebSockets)
* Role-based Access Control
* Advanced Analytics Dashboard

---

## 👨‍💻 Author

**Gopinath U**
📍 Chennai, India

---

## 📜 License

This project is open-source and available under the **MIT License**.

---
