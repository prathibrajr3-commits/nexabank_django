# 🏦 NexaBank — Django Banking System
## Full Banking App with Uniquely Styled Pages

Each page has its own completely distinct visual identity:

| Page | Aesthetic | Fonts |
|------|-----------|-------|
| **Home** | Brutalist Editorial — stark B&W, red ticker tape | Bebas Neue + IBM Plex Mono |
| **Login** | Luxury Minimal — cream/gold, split panel serif | Cormorant Garamond + Jost |
| **Register** | Retro Futuristic — neon cyan/magenta on dark grid | Share Tech Mono + Rajdhani |
| **Dashboard** | Command Center — deep navy sidebar, data-dense | DM Sans + DM Mono |
| **Deposit** | Soft Organic — mint greens, rounded, light mode | Plus Jakarta Sans + Fira Code |
| **Withdraw** | Industrial Amber — dark brown/amber, bold condensed | Barlow Condensed + Fira Code |
| **Transfer** | Art Deco — cream/navy/gold, ornamental symmetry | Playfair Display + Lato |
| **Transactions** | Terminal/Hacker — green-on-black CRT, monospace | Share Tech Mono + VT323 |
| **Loans** | Editorial Magazine — warm ivory, expressive type | Libre Baskerville + Outfit |
| **Apply Loan** | Glassmorphism — purple/indigo, live EMI calculator | Nunito + Space Mono |
| **New Account** | Playful Tiles — soft purple, interactive cards | Syne + Instrument Sans |
| **Account Detail** | Clean Professional — white cards, precise table | Inter + JetBrains Mono |

---

## 🚀 Quick Setup

### 1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 2. Install Django
```bash
pip install -r requirements.txt
```

### 3. Run migrations
```bash
python manage.py makemigrations banking
python manage.py migrate
```

### 4. Create admin superuser
```bash
python manage.py createsuperuser
```

### 5. Start server
```bash
python manage.py runserver
```

### 6. Open browser
- **App:** http://127.0.0.1:8000
- **Admin:** http://127.0.0.1:8000/admin

---

## 📁 Project Structure
```
nexabank_django/
├── manage.py
├── requirements.txt
├── nexabank/
│   ├── settings.py
│   └── urls.py
└── banking/
    ├── models.py        # Account, Transaction, Loan
    ├── views.py         # All business logic
    ├── forms.py         # Django form classes
    ├── urls.py          # URL routing
    ├── admin.py         # Admin panel config
    └── templates/banking/
        ├── home.html          # Brutalist editorial
        ├── login.html         # Luxury minimal
        ├── register.html      # Retro futuristic
        ├── dashboard.html     # Command center
        ├── deposit.html       # Soft organic mint
        ├── withdraw.html      # Industrial amber
        ├── transfer.html      # Art Deco
        ├── transactions.html  # Hacker terminal
        ├── loans.html         # Editorial magazine
        ├── apply_loan.html    # Glassmorphism
        ├── new_account.html   # Playful tiles
        └── account_detail.html # Clean professional
```

## Features
- ✅ User registration & login (Django auth)
- ✅ Multiple account types (Savings, Checking, Fixed Deposit)
- ✅ Deposits & withdrawals with atomic DB transactions
- ✅ Fund transfers between accounts
- ✅ Full transaction history with type filtering
- ✅ Loan applications with live EMI calculator
- ✅ Django admin panel with loan approval
- ✅ 12 uniquely designed pages
