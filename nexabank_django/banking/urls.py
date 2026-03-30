from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/new/', views.new_account, name='new_account'),
    path('accounts/<int:pk>/', views.account_detail, name='account_detail'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transfer/', views.transfer, name='transfer'),
    path('transactions/', views.transactions, name='transactions'),
    path('loans/', views.loans, name='loans'),
    path('loans/apply/', views.apply_loan, name='apply_loan'),
]
