from django.urls import path,include
from .views import *
from user.views import *

app_name= 'api'

urlpatterns = [
    # path('create/account/', AccountsCreateList.as_view()),
    path('create/account/', create_account),
    # path('user-accounts/<id>/', user_accounts),
    path('wallet-details/<id>/', wallet_details),
    path('add-transactions/', account_transactions),
    path('monthly-income/', monthly_income),
    path('monthly-expense/', monthly_expense),
    path('budget-new/', new_budget),
    path('current-budget/', current_budget),
    path('chart-income/', chart_info_income),
    path('chart-expense/', chart_info_expense),
    path('register-user', register_user),
    path('logout/blacklist/', blacklist_token_view), 
]
