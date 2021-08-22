from django.contrib import admin
from .models import *

admin.site.register(BankAccount)
admin.site.register(Transactions)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Budget)
