from django.contrib import admin
from .models import Account, Transaction, Loan


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'user', 'account_type', 'balance', 'status', 'created_at']
    list_filter = ['account_type', 'status']
    search_fields = ['account_number', 'user__username', 'user__email']
    readonly_fields = ['account_number', 'created_at', 'updated_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'account', 'transaction_type', 'amount', 'balance_after', 'status', 'timestamp']
    list_filter = ['transaction_type', 'status']
    search_fields = ['account__account_number', 'description']
    readonly_fields = ['transaction_id', 'timestamp']


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['account', 'loan_type', 'principal_amount', 'interest_rate', 'tenure_months', 'status', 'applied_at']
    list_filter = ['loan_type', 'status']
    search_fields = ['account__account_number', 'account__user__username']
    actions = ['approve_loans', 'reject_loans']

    def approve_loans(self, request, queryset):
        from django.utils import timezone
        queryset.filter(status='PENDING').update(status='APPROVED', approved_at=timezone.now())
    approve_loans.short_description = "Approve selected loans"

    def reject_loans(self, request, queryset):
        queryset.filter(status='PENDING').update(status='REJECTED')
    reject_loans.short_description = "Reject selected loans"
