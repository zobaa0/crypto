from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dashboard.models import Subscription, Withdrawal, Wallet
from .forms import (BasicInfo, AddressInfo, DeleteAccount, 
                    DepositForm, WalletForm, WithdrawalForm)
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta, date
from django.db.models import F, Sum
from account.models import Referral
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from crypto import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

UserModel = get_user_model()
today = date.today()

# Create your views here.
@login_required(login_url='account:login')
def dashboard(request):
    user = UserModel.objects.get(pk=request.user.pk)
    last_deposit = Subscription.objects.filter(user=user, status="Confirmed").last()
    last_withdrawal = Withdrawal.objects.filter(user=user, status="Confirmed").last()
    deposit = Subscription.objects.all()
    withdrawal = Withdrawal.objects.all()
    # TOTAL DEPOSITS
    tot_deposit = sum([i.sub_amount for i in deposit if i.user==user and i.status=="Confirmed"])
    # PENDING DEPOSITS
    pend_deposit = sum([i.sub_amount for i in deposit if i.user==user and i.status=="Pending"])
    # TOTAL WITHDRAWALS
    tot_withdraw = sum([i.amount for i in withdrawal if i.user==user and i.status=="Confirmed"])
    # PENDING WITHDRAWALS
    pend_withdraw = sum([i.amount for i in withdrawal if i.user==user and i.status=="Pending"])
    # TOTAL BALANCE
    total_balance = user.balance
    # EARNED PROFIT
    earned_total = user.profit

    context = {
        'tot_bal': total_balance,
        'tot_earned': earned_total,
        'last_deposit': last_deposit,
        'tot_deposit': tot_deposit,
        'pend_deposit': pend_deposit,
        'last_withdraw': last_withdrawal,
        'pend_withdraw': pend_withdraw,
        'tot_withdraw': tot_withdraw,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required(login_url='account:login')
def profile(request):
    """Update User's Profile"""
    basic_info = BasicInfo(instance=request.user)
    address_info = AddressInfo(instance=request.user)
    delete_account = DeleteAccount(instance=request.user)
    if request.method == 'POST':
        if "form1" in request.POST:
            basic_info = BasicInfo(request.POST, instance=request.user)
            if basic_info.is_valid():
                basic_info.save()
                messages.success(request, ("Your <b>Basic info</b> has been updated!"))
                return redirect('dashboard:profile')
        if 'form2' in request.POST:   
            address_info = AddressInfo(request.POST, instance=request.user)
            if address_info.is_valid():
                address_info.save()
                messages.success(request, ("Your <b>Address info</b> has updated!"))
                return redirect('dashboard:profile')
        if 'form3' in request.POST:
            delete_account = DeleteAccount(request.POST, instance=request.user)
            if delete_account.is_valid():
                deactivate_user = delete_account.save(commit=False)
                del_user = delete_account.cleaned_data['del_account']
                deactivate_user.save()
                if del_user:
                    messages.info(request, ("Your account has been deactivated. \n \
                                            Contact us for reactivation."))   
                    # SEND MAIL    
                    return redirect('main:contact')
    context = {
        'basic_info': basic_info,
        'address_info': address_info,
        'delete_account': delete_account
    }
    return render(request, 'dashboard/profile.html', context)

# Helper Function
def get_ip_address(request):
    """Function to get user's ip address"""
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', None)
    return ip


@login_required(login_url='account:login')
def deposit(request):
    """Function to allow investors make deposit"""
    user = get_object_or_404(UserModel, pk=request.user.pk)
    subscription = Subscription(user=user)
    if request.method == 'POST':
        form = DepositForm(request.POST,instance=subscription)
        if form.is_valid():
            subscribe = form.save(commit=False)
            plan = form.cleaned_data['plan']
            method = form.cleaned_data['sub_method']
            currency = form.cleaned_data['sub_currency']
            amount = form.cleaned_data['sub_amount']
            if method == "Account":
                subscribe.active = True
                subscribe.save()
                messages.success(request, ("Transaction Successful!"))
                return redirect('dashboard:dashboard')
            else:
                # TODO: SEND CONFIRMATION MAIL TO USER
                name = user.username
                context = ({
                    'user': name,
                    'amount': amount,
                    'currency': currency
                })
                # # TODO: SEND CONFIRMATION MAIL TO USER
                # html_version = './dashboard/mails/inactive_dep.html'
                # html_message = render_to_string(html_version, context)
                # subject = 'beeLabbs - Deposit Request'
                # message = EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
                # message.content_subtype = 'html'
                # message.send()
                # TODO: SEND CONFIRMATION MAIL TO ADMIN
                admin_msg = f'Hello Admin,\n\n{name.capitalize()} just initiated a deposit request of ${amount} via {subscription.get_sub_currency_display()}.'
                admin_msg += f'\n\nKindly keep an eye out for the deposit, and confirm the transaction in the admin portal.'
                admin_msg += f'\nTo do that, navigate to the Subscription table, click on the user and toggle on the active button.'
                admin_msg += f'\n\nRegards,\nDevTeam.'
                message1 = EmailMessage(
                    subject = f"User Deposit Notification",
                    body = admin_msg,
                    from_email = 'admin@gmail.com',
                    to = ['admin@gmail.com'],
                )
                message1.send()

                if currency == "Btc":
                    subscribe.save()
                    return redirect('dashboard:btc')
                elif currency == "Eth":
                    subscribe.save()
                    return redirect('dashboard:eth')
                else:
                    subscribe.save()
                    return redirect('dashboard:trc')
    else:
        form = DepositForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/deposit.html', context)


@login_required(login_url='account:login')
def deposit_btc(request):
    user = request.user
    plan = Subscription.objects.filter(user=user, sub_currency="Btc" ).last()
    context = {'plan': plan}
    return render(request, 'dashboard/deposit/btc.html', context)


@login_required(login_url='account:login')
def deposit_eth(request):
    user = request.user
    plan = Subscription.objects.filter(user=user, sub_currency="Eth" ).last()
    context = {'plan': plan}
    return render(request, 'dashboard/deposit/eth.html', context)


@login_required(login_url='account:login')
def deposit_trc(request):
    user = request.user
    plan = Subscription.objects.filter(user=user, sub_currency="Trc20" ).last()
    context = {'plan': plan}
    return render(request, 'dashboard/deposit/trc.html', context)


@login_required(login_url='account:login')
def withdraw(request):
    user=request.user
    # sub = Subscription(user=user)
    withdraw = Withdrawal(user=user)
    if request.method == 'POST':
        form = WithdrawalForm(request.POST, instance=withdraw, user=user)
        if form.is_valid():
            form.save()
            amount = form.cleaned_data['amount']
            wallet = form.cleaned_data['wallet']
            name = user.username
            # TODO: SEND CONFIRMATION MAIL TO USER
            context = ({
                'user': name,
                'amount': amount,
                'wallet': wallet.type,
                'address': wallet.address
            })
            # html_version = './dashboard/mails/inactive_with.html'
            # html_message = render_to_string(html_version, context)
            # subject = 'beeLabbs - Withdrawal Request'
            # message = EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
            # message.content_subtype = 'html'
            # message.send()
            # TODO: SEND CONFIRMATION MAIL TO ADMIN
            admin_msg = f'Hello Admin,\n\n{name.capitalize()} just initiated a withdrawal request.'
            admin_msg += f"\n\nKindly review the withdrawal request. And, if everything seems okay, "
            admin_msg += f"send the required amount to {name.capitalize()} specified address."
            admin_msg += f"\n\nAmount: ${amount}.00\nWallet type: {wallet.get_type_display()}\nWallet address: {wallet.address}"
            admin_msg += f"\n\nOnce that is done, confirm the transaction via the admin panel."
            admin_msg += f"\nTo do that, navigate to the Withdrawal table, click on the user and change the status from 'Pending' to 'Confirmed'."
            admin_msg += f'\n\nRegards,\nDevTeam.'
            message1 = EmailMessage(
                subject = f"User Withdrawal Notification",
                body = admin_msg,
                from_email = 'admin@gmail.com',
                to = ['admin@gmail.com'],
            )
            message1.send()
            messages.success(request, ("Your withdrawal request will be approved once it's verified on the blockchain network."))
            return redirect('dashboard:dashboard')
    else:
        form = WithdrawalForm(user=user)
    context = {
        'form': form
    }
    return render(request, 'dashboard/withdraw.html', context)


@login_required(login_url='account:login')
def wallet(request):
    user = request.user
    wallet=Wallet(user=user)
    object_list = Wallet.objects.filter(user=user)
    # Paginator
    paginator = Paginator(object_list, 2)  # 5 contents per page
    page = request.GET.get('page') # Get the total no. of pages
    try:
        ref = paginator.page(page)
    except PageNotAnInteger:
        # Deliver the first page if page is not an int.
        ref = paginator.page(1)
    except EmptyPage:
        # Deliver last page, if page is out of range
        ref = paginator.page(paginator.num_pages)
    # objectt = Wallet.objects.filter(user=user)
    # if pk:
    #     ref = Wallet.objects.get(pk=pk)
        # print(refe)
    # refe = objectt
    
    # if request.method == 'POST':
    #     if 'delete' in request.POST:
    #         wallet_id = request.POST.get("delete")
    #         wallet=Wallet.objects.get(pk=wallet_id).delete()
    #         return redirect('dashboard:wallet')
    #         pass
        if 'add' in request.POST:
            form = WalletForm(request.POST, instance=wallet)
            if form.is_valid():
                form.save()
                messages.success(request, ("New wallet address successfully added."))
                return redirect("dashboard:wallet")
    else:
        form = WalletForm(instance=user)
    context = {
        'form': form,
        'ref': ref,
        # 'refe': refe
        # 'del_wallet': del_wallet
    }
    return render(request, 'dashboard/wallet.html', context)


@login_required(login_url='account:login')
def logout_request(request):
		logout(request)
		# messages.info(request, 'You have successfully logged out')
		return redirect('account:login')


@login_required(login_url='account:login')
def tot_deposit(request):
    user = request.user
    object_list = Subscription.objects.filter(user=user).order_by('-initiated_on')
    # Paginator
    paginator = Paginator(object_list, 5)  # 5 contents per page
    page = request.GET.get('page') # Get the total no. of pages
    try:
        sub = paginator.page(page)
    except PageNotAnInteger:
        # Deliver the first page if page is not an int.
        sub = paginator.page(1)
    except EmptyPage:
        # Deliver last page, if page is out of range
        sub = paginator.page(paginator.num_pages)
    context = {
        'sub': sub,
        'page': page
    }
    return render(request, 'dashboard/tot_deposit.html', context)


@login_required(login_url='account:login')
def tot_withdraw(request):
    user = request.user
    object_list = Withdrawal.objects.filter(user=user).order_by('-initiated_on')
    # Paginator
    paginator = Paginator(object_list, 5)  # 5 contents per page
    page = request.GET.get('page') # Get the total no. of pages
    try:
        withdraw = paginator.page(page)
    except PageNotAnInteger:
        # Deliver the first page if page is not an int.
        withdraw = paginator.page(1)
    except EmptyPage:
        # Deliver last page, if page is out of range
        withdraw = paginator.page(paginator.num_pages)
    context = {
        'withdraw': withdraw,
        'page': page
    }
    return render(request, 'dashboard/tot_withdraw.html', context)


@login_required(login_url='account:login')
def my_referrals(request):
    referral = Referral.objects.get(user=request.user)
    object_list = referral.get_recommend_profiles()
    paginator = Paginator(object_list, 5)  # 5 referrals per page
    page = request.GET.get('page') # Get the total no. of pages
    try:
        total_recs = paginator.page(page)
    except PageNotAnInteger:
        # Deliver the first page if page is not an int.
        total_recs = paginator.page(1)
    except EmptyPage:
        # Deliver last page, if page is out of range
        total_recs = paginator.page(paginator.num_pages)
    context = {
        'referrals': total_recs,
        'page': page
    }
    return render(request, 'dashboard/referral.html', context)