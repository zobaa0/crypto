from django.urls import path
from .views import *

app_name = "account"

urlpatterns = [
    path('signup/<str:ref_code>/', register, name="register"),
    path('signup', register, name="register"),
    path('login', login_request, name="login"), 
    path('dashboard/password-change', security, name="security"),
]

