from rest_framework import generics, status
from .serializers import *
from budget.models import *
from rest_framework.decorators import api_view,permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.utils import timezone
from user.models import User
from rest_framework import permissions,decorators
import datetime


class AccountsCreateList(generics.ListCreateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = AccountSerializer

@api_view(['POST', 'GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_account(request):
    if request.method == 'POST':
        serializer = CreateAccountSerializer(data=request.data)
        if serializer.is_valid():
            bank = request.data.get('bank')
            account_number = request.data.get('account_number')
            try:
                bank = BankAccount.objects.get(bank=bank, account_number=account_number, created_by=request.user)
                if bank:
                    data = {
                        'error':'Account with this number already exists'
                    }
                    return Response(data)
            except BankAccount.DoesNotExist:
                new_account = BankAccount.objects.create(bank=bank, account_number=account_number, created_by=request.user)
                return Response(AccountSerializer(new_account).data, status=status.HTTP_201_CREATED)
            print("success")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        accounts = BankAccount.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def account_transactions(request):

    if request.method == 'POST':
        serializer = MakeTransactionSerializer(data=request.data, many=False)
        if serializer.is_valid():
            try:
                account = BankAccount.objects.get(id=request.data.get('account'))
            except BankAccount.DoesNotExist:
                return Response({'Invalid': 'Account does not exist. Please Add Account'}, status=status.HTTP_400_BAD_REQUEST)
            amount=request.data.get('amount')
            trans_type=request.data.get('type')
            reason=request.data.get('reason')
            new_transcation = Transactions.objects.create(
                account=BankAccount.objects.get(id=request.data.get('account')),
                amount=amount,
                type=trans_type,
                reason=reason,
                )
            if new_transcation.type == "INCOME":
                new_income = Income.objects.create(
                    account = BankAccount.objects.get(id=request.data.get('account')),
                    amount = float(new_transcation.amount),
                    description=new_transcation.reason,
                )
                if new_income.account.amount_available == None:
                    new_income.account.amount_available = 0.0
                new_income.account.amount_available = float(new_income.account.amount_available) + float(new_income.amount)  
                new_income.account.save()
            elif new_transcation.type == "EXPENSE":
                current_month = timezone.now().month
                current_year = timezone.now().year
                
                new_expense = Expense.objects.create(
                    account = BankAccount.objects.get(id=request.data.get('account')),
                    amount = float(new_transcation.amount),
                    description=new_transcation.reason,
                )

                if new_expense.account.amount_available == None:
                    new_expense.account.amount_available = 0.0
                
                try:
                    if new_expense.account.amount_available < new_transcation.amount:
                        return Response({'error': 'You do not have enought funds for this Expense'}, status=status.HTTP_400_BAD_REQUEST)
                except:pass
                budget=Budget.objects.get(created_at__month=timezone.now().month)
                new_expense.account.amount_available = float(new_expense.account.amount_available) - float(new_expense.amount)
                new_expense.account.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    if request.method == 'GET':
        transactions = Transactions.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def wallet_details(request, id):
    if request.method == 'GET':
        account = BankAccount.objects.get(id=id)
        transactions = Transactions.objects.filter(account=account)
        serializer = AccountTransactionsSerializer(account)
        print(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def monthly_income(request):

    if request.method == 'GET':
        total_monthly_income = 0
        current_month = timezone.now().month
        current_year = timezone.now().year
        try:
            monthly_income = Income.objects.filter(date__year=current_year, date__month=current_month)  
            if monthly_income.count() == 0:
                return Response({'status': 'You have no income'})
        except Income.DoesNotExist:
            pass
        serializer = IncomeSerializer(monthly_income, many=True)
        for income in monthly_income:
            total_monthly_income += income.amount
        return Response({
            "total_income": total_monthly_income,
            "current_month": current_month,
            "current_year": current_year,
            "monthly_income": serializer.data,
            }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def monthly_expense(request):

    if request.method == 'GET':
        total_monthly_expense = 0
        current_month = timezone.now().month
        current_year = timezone.now().year
        try:
            monthly_expense = Expense.objects.filter(date__year=current_year, date__month=current_month)
            if monthly_expense.count() == 0:
                return Response({'status': 'You have no expense'})
        except Expense.DoesNotExist:
            pass
        serializer = ExpenseSerializer(monthly_expense, many=True)
        for income in monthly_expense:
            total_monthly_expense += income.amount
        
        return Response({
            "total_expense": total_monthly_expense,
            "current_month": current_month,
            "current_year": current_year,
            "monthly_expense": serializer.data,
            }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def new_budget(request):
    if request.method == 'POST':
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            budget = Budget.objects.create(
                amount = request.data.get('amount'),
                month = request.data.get('month'),
            )
            return Response(BudgetSerializer(budget).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def current_budget(request):
    
    if request.method == 'GET':
        current_month = timezone.now().month
        current_year = timezone.now().year
        try:
            budget = Budget.objects.get(month=current_month, created_at__year=current_year) 
        except Budget.DoesNotExist:
            return Response({'error': 'You have no budget'})
        serializer = BudgetSerializer(budget)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def chart_info_income(request):
    current_year = timezone.now().year
    jan_income = 0
    feb_income = 0
    mar_income = 0
    apr_income = 0
    may_income = 0
    jun_income = 0
    jul_income = 0
    aug_income = 0
    sept_income = 0
    oct_income = 0
    nov_income= 0
    dec_income=0
    jan_month = Income.objects.filter(date__year=current_year, date__month=1)
    for income in jan_month:
        if income.amount == None:
            income.amount = 0
        jan_income += income.amount

    feb_month = Income.objects.filter(date__year=current_year, date__month=2)
    for income in feb_month:
        if income.amount == None:
            income.amount = 0
        feb_income += income.amount

    mar_month = Income.objects.filter(date__year=current_year, date__month=3)
    for income in mar_month:
        if income.amount == None:
            income.amount = 0
        mar_income += income.amount

    apr_month = Income.objects.filter(date__year=current_year, date__month=4)
    for income in apr_month:
        if income.amount == None:
            income.amount = 0
        apr_income += income.amount

    may_month = Income.objects.filter(date__year=current_year, date__month=5)
    for income in may_month:
        if income.amount == None:
            income.amount = 0
        may_income += income.amount

    jun_month = Income.objects.filter(date__year=current_year, date__month=6)
    for income in jun_month:
        if income.amount == None:
            income.amount = 0
        jun_income += income.amount

    jul_month = Income.objects.filter(date__year=current_year, date__month=7)
    for income in jul_month:
        if income.amount == None:
            income.amount = 0
        jul_income += income.amount

    aug_month = Income.objects.filter(date__year=current_year, date__month=8)
    for income in aug_month:
        if income.amount == None:
            income.amount = 0
        aug_income += income.amount

    sept_month = Income.objects.filter(date__year=current_year, date__month=9)
    for income in sept_month:
        if income.amount == None:
            income.amount = 0
        sept_income += income.amount

    oct_month = Income.objects.filter(date__year=current_year, date__month=10)
    for income in oct_month:
        if income.amount == None:
            income.amount = 0
        oct_income += income.amount

    nov_month = Income.objects.filter(date__year=current_year, date__month=11)
    for income in nov_month:
        if income.amount == None:
            income.amount = 0
        nov_income += income.amount

    dec_month = Income.objects.filter(date__year=current_year, date__month=12)
    for income in dec_month:
        if income.amount == None:
            income.amount = 0
        dec_income += income.amount

    return Response(
        {"income":[jan_income,feb_income,mar_income,apr_income,may_income,jun_income,jul_income,aug_income,sept_income,oct_income,nov_income,dec_income
        ]}, status=status.HTTP_200_OK) 

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def chart_info_expense(request):
    current_year = timezone.now().year
    jan_expense = 0
    feb_expense = 0
    mar_expense = 0
    apr_expense = 0
    may_expense = 0
    jun_expense = 0
    jul_expense = 0
    aug_expense = 0
    sept_expense = 0
    oct_expense = 0
    nov_expense= 0
    dec_expense=0
    jan_month = Expense.objects.filter(date__year=current_year, date__month=1)
    for expense in jan_month:
        if expense.amount == None:
            expense.amount = 0
        jan_expense += expense.amount

    feb_month = Expense.objects.filter(date__year=current_year, date__month=2)
    for expense in feb_month:
        if expense.amount == None:
            expense.amount = 0
        feb_expense += expense.amount

    mar_month = Expense.objects.filter(date__year=current_year, date__month=3)
    for expense in mar_month:
        if expense.amount == None:
            expense.amount = 0
        mar_expense += expense.amount

    apr_month = Expense.objects.filter(date__year=current_year, date__month=4)
    for expense in apr_month:
        if expense.amount == None:
            expense.amount = 0
        apr_expense += expense.amount

    may_month = Expense.objects.filter(date__year=current_year, date__month=5)
    for expense in may_month:
        if expense.amount == None:
            expense.amount = 0
        may_expense += expense.amount

    jun_month = Expense.objects.filter(date__year=current_year, date__month=6)
    for expense in jun_month:
        if expense.amount == None:
            expense.amount = 0
        jun_expense += expense.amount

    jul_month = Expense.objects.filter(date__year=current_year, date__month=7)
    for expense in jul_month:
        if expense.amount == None:
            expense.amount = 0
        jul_expense += expense.amount

    aug_month = Expense.objects.filter(date__year=current_year, date__month=8)
    for expense in aug_month:
        if expense.amount == None:
            expense.amount = 0
        aug_expense += expense.amount

    sept_month = Expense.objects.filter(date__year=current_year, date__month=9)
    for expense in sept_month:
        if expense.amount == None:
            expense.amount = 0
        sept_expense += expense.amount

    oct_month = Expense.objects.filter(date__year=current_year, date__month=10)
    for expense in oct_month:
        if expense.amount == None:
            expense.amount = 0
        oct_expense += expense.amount

    nov_month = Expense.objects.filter(date__year=current_year, date__month=11)
    for expense in nov_month:
        if expense.amount == None:
            expense.amount = 0
        nov_expense += expense.amount

    dec_month = Expense.objects.filter(date__year=current_year, date__month=12)
    for expense in dec_month:
        if expense.amount == None:
            expense.amount = 0
        dec_expense += expense.amount 
    
    return Response(
        {"expense":[jan_expense,feb_expense,mar_expense,apr_expense,may_expense,jun_expense,jul_expense,aug_expense,sept_expense,oct_expense,nov_expense,dec_expense]}, status=status.HTTP_200_OK) 

