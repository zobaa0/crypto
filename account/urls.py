from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    path('signup/<str:ref_code>/', register, name="register"),
    path('signup/', register, name="register"),
    path('login/', login_request, name="login"), 
    path('dashboard/password-change/', security, name="security"),
    path('password_reset/', reset_password, name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confirm.html', success_url='/login/'), name='password_reset_confirm'),
]