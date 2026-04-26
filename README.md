# 🏛️ College Event Portal System
### ZIBACAR – Zeal Institute of Business Administration, Computer Application and Research
**Mini Project | MCA Sem-I | By: Shivam Bhikan Chavan & Prachi Babarao Ganesh**
**Guide: Prof. Kirti Samrit**

---

## 🚀 Quick Start (3 Steps)

### Step 1 – Install Django
```bash
pip install django
```

### Step 2 – Run Setup Script
```bash
python setup.py
```
This will:
- Create the SQLite database
- Apply all migrations
- Create admin user (`admin` / `admin123`)
- Seed 3 sample halls

### Step 3 – Start the Server
```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

---

## 🔗 URL Routes

| URL | Description |
|-----|-------------|
| `/` | Home – browse available halls |
| `/book/<id>/` | Book a specific hall |
| `/my-bookings/` | View bookings by email |
| `/cancel/<id>/` | Cancel a pending booking |
| `/login/` | User login |
| `/logout/` | Logout |
| `/register/` | Create a new account |
| `/dashboard/` | Admin booking dashboard *(staff only)* |
| `/dashboard/halls/` | Manage halls *(staff only)* |
| `/dashboard/halls/add/` | Add new hall *(staff only)* |
| `/admin/` | Django built-in admin panel |

---

## 👤 Default Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.x + Django 4.x |
| Database | SQLite (development) / MongoDB via Djongo (production) |
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |
| Auth | Django's built-in authentication system |

---

## 📁 Project Structure

```
college_event_portal/
├── manage.py
├── setup.py               ← Run this first!
├── requirements.txt
├── README.md
│
├── college_event_portal/  ← Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── halls/                 ← Main app
    ├── models.py          ← Hall, Booking, UserProfile
    ├── views.py           ← All view logic
    ├── urls.py            ← URL routing
    ├── admin.py           ← Django admin config
    ├── migrations/
    └── templates/halls/   ← All HTML templates
        ├── base.html
        ├── index.html
        ├── book_hall.html
        ├── my_bookings.html
        ├── login.html
        ├── register.html
        ├── admin_dashboard.html
        ├── manage_halls.html
        ├── add_hall.html
        ├── edit_hall.html
        └── booking_detail.html
```

---

## ✨ Features

### For Students / Faculty (Public)
- Browse all available halls with details (capacity, location, facilities)
- Book a hall by submitting a form (no login required)
- View bookings by entering your email address
- Cancel pending bookings

### For Registered Users
- Register & login to auto-fill booking forms
- View personal booking history

### For Admin (Staff)
- **Custom Dashboard** at `/dashboard/` with:
  - Booking statistics (Total / Pending / Approved / Rejected)
  - Advanced filters (Status, User Type, Hall, Date Range, Search)
  - One-click Approve / Reject bookings
- **Hall Management** at `/dashboard/halls/`:
  - Add, Edit, Delete halls
  - Toggle hall availability
- **Django Admin** at `/admin/` with bulk actions

---

## 🗃️ Database Tables

| Table | Purpose |
|-------|---------|
| `auth_user` | Django's built-in user accounts |
| `halls_userprofile` | Extended user info (type: student/faculty) |
| `halls_hall` | Hall details (name, capacity, location, facilities) |
| `halls_booking` | Booking records with status tracking |

---

## 🔒 Business Rules
- Bookings default to **Pending** status
- Only **admin** can approve or reject
- Only **pending** bookings can be cancelled
- Conflict check prevents double-booking the same hall & time
- Students / Faculty can book without creating an account

---

## 📞 Support
For issues, contact the development team at ZIBACAR, Narhe, Pune – 411041.
