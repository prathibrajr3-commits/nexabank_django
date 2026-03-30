Optimizing tool selection...Checking the main project README and key files to summarize what this workspace contains.

Searched for files matching `**/manage.py`, 2 matches

Read [](file:///c%3A/Users/DELL7420/Downloads/nexabank_django/nexabank_django/README.md)

Read [](file:///c%3A/Users/DELL7420/Downloads/nexabank_django/banking_system/README.md)

## Project Overview

This workspace contains two Django banking applications:

1. banking_system
2. nexabank_django

Both are full-featured banking systems with:
- user registration/login
- multiple account types
- deposits, withdrawals, transfers
- transaction history
- loan application handling
- Django admin support

---

## What each project includes

### banking_system
- manage.py
- `requirements.txt`
- `banking_project/` – Django settings, URLs, WSGI
- `banking/` app – models, views, forms, URLs, admin
- `templates/banking/` – pages for home, dashboard, deposit, withdraw, transfer, loans, account details, create account, etc.

### nexabank_django
- manage.py
- `requirements.txt`
- `nexabank/` – Django settings and URLs
- `banking/` app – same core banking logic
- `banking/templates/banking/` – similar banking UI pages plus `new_account.html`

---

## Key features
- Authentication
- Account management
- Fund transfer
- Transaction tracking
- Loan application flow
- Admin loan approval

---

## How to run
From either project folder:
1. Activate the virtual environment
2. `pip install -r requirements.txt`
3. `python manage.py makemigrations`
4. `python manage.py migrate`
5. `python manage.py runserver`

This is essentially a Django-based banking web app with account and loan functionality, built around a clean UI and admin backend.
