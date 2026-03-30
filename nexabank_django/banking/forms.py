from django import forms
from django.contrib.auth.models import User
from .models import Account, Loan

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']
    def clean(self):
        d = super().clean()
        if d.get('password') != d.get('confirm_password'):
            raise forms.ValidationError('Passwords do not match.')
        return d
    def clean_username(self):
        u = self.cleaned_data.get('username')
        if User.objects.filter(username=u).exists(): raise forms.ValidationError('Username taken.')
        return u

class DepositForm(forms.Form):
    account = forms.ModelChoiceField(queryset=Account.objects.none())
    amount = forms.DecimalField(max_digits=15, decimal_places=2, min_value=0.01)
    description = forms.CharField(max_length=255, required=False)
    def __init__(self, *a, **kw):
        user = kw.pop('user'); super().__init__(*a, **kw)
        self.fields['account'].queryset = Account.objects.filter(user=user, status='ACTIVE')

class WithdrawForm(forms.Form):
    account = forms.ModelChoiceField(queryset=Account.objects.none())
    amount = forms.DecimalField(max_digits=15, decimal_places=2, min_value=0.01)
    description = forms.CharField(max_length=255, required=False)
    def __init__(self, *a, **kw):
        user = kw.pop('user'); super().__init__(*a, **kw)
        self.fields['account'].queryset = Account.objects.filter(user=user, status='ACTIVE')

class TransferForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=Account.objects.none())
    to_account_number = forms.CharField(max_length=20)
    amount = forms.DecimalField(max_digits=15, decimal_places=2, min_value=0.01)
    description = forms.CharField(max_length=255, required=False)
    def __init__(self, *a, **kw):
        user = kw.pop('user'); super().__init__(*a, **kw)
        self.fields['from_account'].queryset = Account.objects.filter(user=user, status='ACTIVE')

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['account','loan_type','principal_amount','interest_rate','tenure_months']
    def __init__(self, *a, **kw):
        user = kw.pop('user'); super().__init__(*a, **kw)
        self.fields['account'].queryset = Account.objects.filter(user=user, status='ACTIVE')
