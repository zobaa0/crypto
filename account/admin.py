from django.contrib import admin
from .models import CustomUser, Referral

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Referral)
