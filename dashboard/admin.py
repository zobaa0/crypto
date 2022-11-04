from django.contrib import admin
from .models import Plan, Subscription, Withdrawal, Wallet

# Register your models here.
admin.site.register(Plan)
admin.site.register(Subscription)
admin.site.register(Wallet)
admin.site.register(Withdrawal)
# admin.site.register(Min_withdraw)
# admin.site.register(Transaction)