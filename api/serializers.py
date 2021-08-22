from budget.models import BankAccount, Transactions
from rest_framework import fields, serializers
from budget.models import *



class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['bank', 'account_number']


class TransactionSerializer(serializers.ModelSerializer):
    # month = serializers.ReadOnlyField(source="date__month")
    # year = serializers.ReadOnlyField(source="date__year")
    date = serializers.DateTimeField(format="%Y-%m-%d")
    class Meta:
        model = Transactions
        fields = ['account', 'amount', 'type', 'reason', 'date' ]

class AccountSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer("source=transaction", many=True)
    
    class Meta:
        model = BankAccount
        fields = ['id','bank', 'account_number', 'amount_available', 'date_added', 'transaction']


class MakeTransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transactions
        fields = ['account', 'amount', 'type', 'reason']


class AccountTransactionsSerializer(serializers.ModelSerializer):
    # date = serializers.DateTimeField(format="%Y-%m-%d")
    transaction = TransactionSerializer('source=transaction', many=True)

    class Meta:
        model = BankAccount
        fields = ['bank', 'transaction']


class MonthYearSerializer(serializers.ModelSerializer):

    date__month = serializers.ReadOnlyField()
    date__year = serializers.ReadOnlyField()

    class Meta:
        model = Transactions
        fields = ("date__month", "date__year")

class ExpenseSerializer(serializers.ModelSerializer):
    account = CreateAccountSerializer("source=account")
    date = serializers.DateTimeField(format="%Y-%m-%d")
    class Meta:
        model = Expense
        fields = ['account', 'amount', 'date', 'description']


class IncomeSerializer(serializers.ModelSerializer):
    account = CreateAccountSerializer("source=account")
    date = serializers.DateTimeField(format="%Y-%m-%d")
    class Meta:
        model = Income
        fields = ['account', 'amount', 'date', 'description']


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['amount', 'month', 'created_at']
