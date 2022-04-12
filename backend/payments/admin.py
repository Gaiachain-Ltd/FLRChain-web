from django.contrib import admin
from payments.models import CirclePayment, CircleTransfer, MTNPayout


class CirclePaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'fee', 'status', 
                    'claimed', 'id')

admin.site.register(CirclePayment, CirclePaymentAdmin)


class CircleTransferAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'id')

admin.site.register(CircleTransfer, CircleTransferAdmin)


class MTNPayoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction', 'amount', 
                    'status', 'id')

admin.site.register(MTNPayout, MTNPayoutAdmin)