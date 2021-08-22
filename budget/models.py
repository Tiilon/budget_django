from django.db import models
from django.utils import timezone
from django.conf import settings

class BankAccount(models.Model):
    bank = models.CharField(max_length=200, blank=True, null=True)
    account_number = models.CharField(max_length=200, blank=True, null=True)
    amount_available = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0.0)
    date_added = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='accounts', on_delete=models.CASCADE)

    class Meta:
        ordering = ('bank',)
        db_table = 'accounts'
        verbose_name = ('account')
        verbose_name_plural = ('accounts')

    def __str__(self):
        return f"{self.bank}"

TYPE = {
    ('EXPENSE', "EXPENSE"),
    ('INCOME' , "INCOME"),
}

class Budget(models.Model):
    amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0.0)
    month = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='budgets', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.month}"

class Income(models.Model):
    account= models.ForeignKey(BankAccount, related_name='income', on_delete=models.CASCADE, blank=True, null=True)
    amount=models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0.0)
    date=models.DateTimeField(default=timezone.now)
    description=models.CharField(max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='incomes', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date',)
        db_table = 'income'
        verbose_name = ('income')
        verbose_name_plural = ('income')

    def __str__(self):
        return f"{self.account.bank} - {self.amount}"

class Expense(models.Model):
    account= models.ForeignKey(BankAccount, related_name='expense', on_delete=models.CASCADE, blank=True, null=True)
    amount=models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0.0)
    date=models.DateTimeField(default=timezone.now)
    description=models.CharField(max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='expenses', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date',)
        db_table = 'expense'
        verbose_name = ('expense')
        verbose_name_plural = ('expense')

    def __str__(self):
        return f"{self.account.bank} - {self.amount}"

class Transactions(models.Model):
    account = models.ForeignKey(BankAccount, related_name='transaction', on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0.0)
    type = models.CharField(max_length=200, blank=True, null=True, choices=TYPE)
    reason = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='transactions', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date',)
        db_table = 'transactions'
        verbose_name = ('transaction')
        verbose_name_plural = ('transactions')

    def __str__(self):
        return f"{self.type}"


