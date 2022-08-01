from django.contrib import admin
from payments.models import CirclePayment, MTNPayout


class CirclePaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'fee', 'status', 
                    'claimed', 'id')

admin.site.register(CirclePayment, CirclePaymentAdmin)


class MTNPayoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction', 'amount', 
                    'status', 'id')

admin.site.register(MTNPayout, MTNPayoutAdmin)