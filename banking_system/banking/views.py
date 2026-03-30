from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction as db_transaction
from django.db.models import Sum, Q
from decimal import Decimal
from .models import Account, Transaction, Loan
from .forms import (
    UserRegistrationForm, AccountCreationForm, DepositForm,
    WithdrawalForm, TransferForm, LoanApplicationForm
)


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'banking/home.html')


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Auto-create a savings account
            Account.objects.create(user=user, account_type='SAVINGS', balance=0)
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'banking/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'banking/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    recent_transactions = Transaction.objects.filter(
        account__user=request.user
    ).select_related('account')[:10]

    total_balance = accounts.aggregate(total=Sum('balance'))['total'] or 0
    active_loans = Loan.objects.filter(account__user=request.user, status='ACTIVE')
    total_loan = active_loans.aggregate(total=Sum('outstanding_amount'))['total'] or 0

    context = {
        'accounts': accounts,
        'recent_transactions': recent_transactions,
        'total_balance': total_balance,
        'total_loan': total_loan,
        'active_loans_count': active_loans.count(),
    }
    return render(request, 'banking/dashboard.html', context)


@login_required
def account_detail(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = account.transactions.all()[:20]
    return render(request, 'banking/account_detail.html', {
        'account': account,
        'transactions': transactions
    })


@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, f'{account.get_account_type_display()} created successfully!')
            return redirect('dashboard')
    else:
        form = AccountCreationForm()
    return render(request, 'banking/create_account.html', {'form': form})


@login_required
def deposit(request):
    accounts = Account.objects.filter(user=request.user, status='ACTIVE')
    if request.method == 'POST':
        form = DepositForm(request.POST, user=request.user)
        if form.is_valid():
            account = form.cleaned_data['account']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data.get('description', 'Deposit')

            with db_transaction.atomic():
                account.balance += Decimal(str(amount))
                account.save()
                Transaction.objects.create(
                    account=account,
                    transaction_type='DEPOSIT',
                    amount=amount,
                    balance_after=account.balance,
                    description=description or 'Cash Deposit',
                    status='COMPLETED'
                )
            messages.success(request, f'${amount} deposited successfully!')
            return redirect('dashboard')
    else:
        form = DepositForm(user=request.user)
    return render(request, 'banking/deposit.html', {'form': form, 'accounts': accounts})


@login_required
def withdraw(request):
    accounts = Account.objects.filter(user=request.user, status='ACTIVE')
    if request.method == 'POST':
        form = WithdrawalForm(request.POST, user=request.user)
        if form.is_valid():
            account = form.cleaned_data['account']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data.get('description', 'Withdrawal')

            if account.balance < Decimal(str(amount)):
                messages.error(request, 'Insufficient funds.')
            else:
                with db_transaction.atomic():
                    account.balance -= Decimal(str(amount))
                    account.save()
                    Transaction.objects.create(
                        account=account,
                        transaction_type='WITHDRAWAL',
                        amount=amount,
                        balance_after=account.balance,
                        description=description or 'Cash Withdrawal',
                        status='COMPLETED'
                    )
                messages.success(request, f'${amount} withdrawn successfully!')
                return redirect('dashboard')
    else:
        form = WithdrawalForm(user=request.user)
    return render(request, 'banking/withdraw.html', {'form': form, 'accounts': accounts})


@login_required
def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST, user=request.user)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account_number = form.cleaned_data['to_account_number']
            amount = Decimal(str(form.cleaned_data['amount']))
            description = form.cleaned_data.get('description', 'Transfer')

            try:
                to_account = Account.objects.get(account_number=to_account_number, status='ACTIVE')
            except Account.DoesNotExist:
                messages.error(request, 'Destination account not found.')
                return render(request, 'banking/transfer.html', {'form': form})

            if from_account.balance < amount:
                messages.error(request, 'Insufficient funds.')
            elif from_account == to_account:
                messages.error(request, 'Cannot transfer to the same account.')
            else:
                with db_transaction.atomic():
                    from_account.balance -= amount
                    from_account.save()
                    to_account.balance += amount
                    to_account.save()

                    Transaction.objects.create(
                        account=from_account,
                        transaction_type='TRANSFER_OUT',
                        amount=amount,
                        balance_after=from_account.balance,
                        related_account=to_account,
                        description=description or f'Transfer to {to_account.account_number}',
                        status='COMPLETED'
                    )
                    Transaction.objects.create(
                        account=to_account,
                        transaction_type='TRANSFER_IN',
                        amount=amount,
                        balance_after=to_account.balance,
                        related_account=from_account,
                        description=description or f'Transfer from {from_account.account_number}',
                        status='COMPLETED'
                    )
                messages.success(request, f'${amount} transferred successfully!')
                return redirect('dashboard')
    else:
        form = TransferForm(user=request.user)
    return render(request, 'banking/transfer.html', {'form': form})


@login_required
def apply_loan(request):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.save()
            messages.success(request, 'Loan application submitted! Pending approval.')
            return redirect('loans')
    else:
        form = LoanApplicationForm(user=request.user)
    return render(request, 'banking/apply_loan.html', {'form': form})


@login_required
def loans(request):
    user_loans = Loan.objects.filter(account__user=request.user).select_related('account')
    return render(request, 'banking/loans.html', {'loans': user_loans})


@login_required
def transactions(request):
    all_transactions = Transaction.objects.filter(
        account__user=request.user
    ).select_related('account', 'related_account')
    return render(request, 'banking/transactions.html', {'transactions': all_transactions})
