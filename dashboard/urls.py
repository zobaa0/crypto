from django.urls import path
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('profile/', profile, name="profile"),
    path('deposit/', deposit, name="deposit"),
    path('deposit/btc/', deposit_btc, name="btc"),
    path('deposit/eth/', deposit_eth, name="eth"),
    path('deposit/trc/', deposit_trc, name="trc"),
    path('withdraw/', withdraw, name="withdraw"),
    path('wallet/', wallet, name="wallet"),
    path('wallet/<int:pk>/delete/', del_wallet, name="del_wallet"),
    path('referrals/', my_referrals, name="referral"),
    path('logout/', logout_request, name="logout"),
    path('deposit/?a=total/', tot_deposit, name="tot_deposit"),
    path('withdraw/?a=total/', tot_withdraw, name="tot_withdraw"),
]