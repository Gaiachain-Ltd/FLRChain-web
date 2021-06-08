from django.contrib import admin
from transactions.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('action', 'from_account', 'to_account', 
                    'currency', 'amount', 'fee', 'status', 
                    'txid', 'created')

admin.site.register(Transaction, TransactionAdmin)
