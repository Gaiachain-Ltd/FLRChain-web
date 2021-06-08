from django.contrib import admin
from payments.models import CirclePayment, CircleTransfer

admin.site.register(CirclePayment)
admin.site.register(CircleTransfer)
