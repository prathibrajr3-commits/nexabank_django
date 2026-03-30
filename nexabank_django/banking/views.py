from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction as db_tx
from django.db.models import Sum
from decimal import Decimal
from .models import Account, Transaction, Loan
from .forms import RegisterForm, DepositForm, WithdrawForm, TransferForm, LoanForm

def home(request):
    if request.user.is_authenticated: return redirect('dashboard')
    return render(request, 'banking/home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(user=user, account_type='SAVINGS')
            login(request, user)
            messages.success(request, f'Welcome to NexaBank, {user.first_name}!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'banking/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user); return redirect('dashboard')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'banking/login.html')

@login_required
def logout_view(request):
    logout(request); return redirect('home')

@login_required
def dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    total_balance = accounts.aggregate(t=Sum('balance'))['t'] or 0
    recent_txs = Transaction.objects.filter(account__user=request.user).select_related('account')[:8]
    active_loans = Loan.objects.filter(account__user=request.user, status__in=['ACTIVE','APPROVED'])
    total_loan = active_loans.aggregate(t=Sum('outstanding_amount'))['t'] or 0
    return render(request, 'banking/dashboard.html', {
        'accounts': accounts, 'total_balance': total_balance,
        'recent_txs': recent_txs, 'active_loans': active_loans, 'total_loan': total_loan,
    })

@login_required
def account_detail(request, pk):
    acc = get_object_or_404(Account, pk=pk, user=request.user)
    txs = acc.transactions.all()[:30]
    return render(request, 'banking/account_detail.html', {'account': acc, 'txs': txs})

@login_required
def new_account(request):
    if request.method == 'POST':
        atype = request.POST.get('account_type')
        if atype in ['SAVINGS','CHECKING','FIXED']:
            Account.objects.create(user=request.user, account_type=atype)
            messages.success(request, 'New account opened!')
            return redirect('dashboard')
    return render(request, 'banking/new_account.html')

@login_required
def deposit(request):
    form = DepositForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        acc = form.cleaned_data['account']; amt = form.cleaned_data['amount']
        with db_tx.atomic():
            acc.balance += amt; acc.save()
            Transaction.objects.create(account=acc, transaction_type='DEPOSIT', amount=amt, balance_after=acc.balance, description=form.cleaned_data.get('description') or 'Deposit')
        messages.success(request, f'${amt} deposited!')
        return redirect('dashboard')
    return render(request, 'banking/deposit.html', {'form': form})

@login_required
def withdraw(request):
    form = WithdrawForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        acc = form.cleaned_data['account']; amt = form.cleaned_data['amount']
        if acc.balance < amt:
            messages.error(request, 'Insufficient funds.')
        else:
            with db_tx.atomic():
                acc.balance -= amt; acc.save()
                Transaction.objects.create(account=acc, transaction_type='WITHDRAWAL', amount=amt, balance_after=acc.balance, description=form.cleaned_data.get('description') or 'Withdrawal')
            messages.success(request, f'${amt} withdrawn!')
            return redirect('dashboard')
    return render(request, 'banking/withdraw.html', {'form': form})

@login_required
def transfer(request):
    form = TransferForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        from_acc = form.cleaned_data['from_account']; amt = Decimal(str(form.cleaned_data['amount']))
        desc = form.cleaned_data.get('description') or ''
        try:
            to_acc = Account.objects.get(account_number=form.cleaned_data['to_account_number'], status='ACTIVE')
        except Account.DoesNotExist:
            messages.error(request, 'Destination account not found.'); return render(request, 'banking/transfer.html', {'form': form})
        if from_acc.balance < amt: messages.error(request, 'Insufficient funds.')
        elif from_acc == to_acc: messages.error(request, 'Cannot transfer to same account.')
        else:
            with db_tx.atomic():
                from_acc.balance -= amt; from_acc.save()
                to_acc.balance += amt; to_acc.save()
                Transaction.objects.create(account=from_acc, transaction_type='TRANSFER_OUT', amount=amt, balance_after=from_acc.balance, related_account=to_acc, description=desc or f'To {to_acc.account_number}')
                Transaction.objects.create(account=to_acc, transaction_type='TRANSFER_IN', amount=amt, balance_after=to_acc.balance, related_account=from_acc, description=desc or f'From {from_acc.account_number}')
            messages.success(request, f'${amt} transferred!')
            return redirect('dashboard')
    return render(request, 'banking/transfer.html', {'form': form})

@login_required
def transactions(request):
    tx_type = request.GET.get('type', '')
    qs = Transaction.objects.filter(account__user=request.user).select_related('account')
    if tx_type: qs = qs.filter(transaction_type=tx_type)
    return render(request, 'banking/transactions.html', {'txs': qs[:150], 'filter': tx_type})

@login_required
def loans(request):
    all_loans = Loan.objects.filter(account__user=request.user).select_related('account')
    return render(request, 'banking/loans.html', {'loans': all_loans})

@login_required
def apply_loan(request):
    form = LoanForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        loan = form.save(); messages.success(request, 'Loan application submitted!')
        return redirect('loans')
    return render(request, 'banking/apply_loan.html', {'form': form})
