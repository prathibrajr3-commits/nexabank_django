from django.contrib import admin
from .models import Account, Transaction, Loan

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_number','user','account_type','balance','status','created_at']
    list_filter = ['account_type','status']
    search_fields = ['account_number','user__username']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id','account','transaction_type','amount','status','timestamp']
    list_filter = ['transaction_type','status']

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['account','loan_type','principal_amount','status','applied_at']
    list_filter = ['status','loan_type']
    actions = ['approve','reject']
    def approve(self, req, qs): qs.update(status='APPROVED')
    def reject(self, req, qs): qs.update(status='REJECTED')
    approve.short_description = 'Approve selected'
    reject.short_description = 'Reject selected'
