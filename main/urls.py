import imp
from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', home, name="home"),
    path('about', about, name="about"),
    path('faq', faq, name="faq"),
    path('privacy', privacy, name="privacy"),
    path('terms', terms, name="terms"),
    path('contact', contact, name="contact"),
    path('services', services, name="services"),
    path('plans', plans, name="plans"),
    path('refund', refund, name="refund"),
    path('how-to-invest', howto, name="howto"),
] 