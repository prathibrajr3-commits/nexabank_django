from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid, random, string

def gen_account_number():
    return ''.join(random.choices(string.digits, k=12))

class Account(models.Model):
    TYPES = [('SAVINGS','Savings'),('CHECKING','Checking'),('FIXED','Fixed Deposit')]
    STATUS = [('ACTIVE','Active'),('FROZEN','Frozen'),('CLOSED','Closed')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True, default=gen_account_number)
    account_type = models.CharField(max_length=10, choices=TYPES, default='SAVINGS')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.account_number} ({self.account_type})"
    class Meta: ordering = ['-created_at']

class Transaction(models.Model):
    TYPES = [('DEPOSIT','Deposit'),('WITHDRAWAL','Withdrawal'),('TRANSFER_IN','Transfer In'),('TRANSFER_OUT','Transfer Out')]
    STATUS = [('COMPLETED','Completed'),('PENDING','Pending'),('FAILED','Failed')]
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    related_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='related_txs')
    status = models.CharField(max_length=10, choices=STATUS, default='COMPLETED')
    timestamp = models.DateTimeField(default=timezone.now)
    class Meta: ordering = ['-timestamp']

class Loan(models.Model):
    TYPES = [('PERSONAL','Personal'),('HOME','Home'),('CAR','Car'),('BUSINESS','Business')]
    STATUS = [('PENDING','Pending'),('APPROVED','Approved'),('REJECTED','Rejected'),('ACTIVE','Active'),('PAID','Paid')]
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='loans')
    loan_type = models.CharField(max_length=10, choices=TYPES)
    principal_amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tenure_months = models.IntegerField()
    monthly_payment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    outstanding_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS, default='PENDING')
    applied_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.monthly_payment:
            r = float(self.interest_rate)/100/12; n = self.tenure_months; p = float(self.principal_amount)
            self.monthly_payment = round(p*r*(1+r)**n/((1+r)**n-1),2) if r>0 else round(p/n,2)
        if not self.outstanding_amount: self.outstanding_amount = self.principal_amount
        super().save(*args, **kwargs)
    class Meta: ordering = ['-applied_at']
