# 🏦 NexaBank — Django Banking System

A full-featured banking system built with Django featuring accounts, transactions, transfers, and loans.

---

## ✅ Features

- **User Auth** — Register, login, logout
- **Multiple Accounts** — Savings, Checking, Fixed Deposit
- **Deposits & Withdrawals** — With full transaction history
- **Fund Transfers** — Between any two NexaBank accounts
- **Loan Management** — Apply, track, live EMI calculator
- **Admin Panel** — Full Django admin with loan approval actions
- **Responsive UI** — Premium dark theme built with pure CSS

---

## 🚀 Setup Instructions

### 1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create superuser (for admin)
```bash
python manage.py createsuperuser
```

### 5. Run the server
```bash
python manage.py runserver
```

### 6. Visit the app
- **App:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/

---

## 📁 Project Structure

```
banking_system/
├── manage.py
├── requirements.txt
├── banking_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── banking/
│   ├── models.py        # Account, Transaction, Loan
│   ├── views.py         # All business logic
│   ├── forms.py         # Django forms
│   ├── urls.py          # URL routing
│   └── admin.py         # Admin panel config
└── templates/
    └── banking/
        ├── base.html
        ├── home.html
        ├── login.html
        ├── register.html
        ├── dashboard.html
        ├── deposit.html
        ├── withdraw.html
        ├── transfer.html
        ├── transactions.html
        ├── loans.html
        ├── apply_loan.html
        ├── account_detail.html
        └── create_account.html
```

---

## 🔐 Admin Panel

Approve or reject loans in bulk from the Django admin at `/admin/banking/loan/`.
