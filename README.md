# GymTech 🏋️

A modern **Gym Management Web Application** built with **Flask, SQLAlchemy, Bootstrap, and SQLite**.
GymTech helps manage **members, plans, employees, trainers, payroll, and inquiries** through a clean admin-friendly interface.

---

## 🚀 Features

### 👤 Authentication & User Management

* User Registration & Login
* Secure password hashing using `werkzeug.security`
* Session-based authentication
* Profile management with image upload
* Role-based access:

  * **Admin**
  * **Member**

---

### 🏋️ Membership & Plans

* Create, update, and delete membership plans
* Dynamic plan cards with feature availability
* Admin-only plan management
* Features supported:

  * Gym Access
  * Cardio Equipment
  * Personal Trainer
  * Diet Plan
  * Group Classes

---

### 👥 Member Management

* Add new members
* Assign plans
* Set membership start & end dates
* Update member details
* Delete members
* Prevent admin self-delete

---

### 👨‍💼 Employee Management

* Add and manage employees
* Employee types:

  * Manager
  * Trainer
  * Receptionist
  * Helper
  * Cleaner
* Auto age calculation from DOB
* Joining date management

---

### 💪 Trainer Management

* Auto trainer record creation when employee type = Trainer
* Trainer categories:

  * General Trainer
  * Personal Trainer
* PT monthly fee support
* Update trainer details from frontend
* Dynamic trainer section on home page

---

### 💰 Salary / Payroll

* Salary records for employees
* Monthly salary tracking
* Credit status update
* Payroll-ready structure for future enhancements

---

### 📩 Contact System

* Contact page with EmailJS integration
* Sends gym inquiries directly via email
* Separate inquiry signatures for GymTech and Portfolio usage

---

## 🛠️ Tech Stack

### Backend

* Flask
* SQLAlchemy
* Flask-Migrate
* SQLite

### Frontend

* HTML
* CSS
* Bootstrap 5
* JavaScript
* Jinja2 Templates

### External Services

* EmailJS

---

## 📂 Project Structure

```bash
GymTech/
│
├── app.py
├── models.py
├── database.db
├── requirements.txt
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── plans.html
│   ├── members.html
│   ├── employee.html
│   ├── trainers.html
│   └── contact.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── migrations/
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/GymTech.git
cd GymTech
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

### 5. Run Application

```bash
python app.py
```

---

## 🔐 Default Roles

Admin features are visible only for users with:

```python
user_type = 'Admin'
```

Members have restricted access.

---

## 🌟 Future Enhancements

* Attendance tracking
* Payment gateway integration
* Trainer schedule management
* Diet plan generator
* Notifications & reminders
* Dashboard analytics
* Reports export (PDF/Excel)

---

## 👨‍💻 Developed By

**Ashutosh Singh**
Full Stack Developer | Solution Developer

---

## 📄 License

This project is for educational and portfolio purposes.