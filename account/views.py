from django.shortcuts import render, redirect
from .forms import NewUserForm, UserLoginForm, PasswordChange
from django.contrib.auth import get_user_model, login, authenticate, update_session_auth_hash
from django.contrib import messages
from main.decorators import user_not_authenticated
from .models import Referral
from django.db.models import F
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from crypto import settings
from django.contrib.auth.decorators import login_required 

userModel = get_user_model()

# Create your views here.
@user_not_authenticated
def register(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        referral = Referral.objects.get(code=code)
        request.session['ref_profile'] = referral.id
    except:
        pass
    referral_id =  request.session.get('ref_profile')
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']

            # TODO: SEND CONFIRMATION MAIL TO USER
            context = ({'username': username, 'email': email})
            html_version = './account/mails/new_user_confirm.html'
            html_message = render_to_string(html_version, context)
            subject = 'Welcome to beeLabbs'
            message = EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
            message.content_subtype = 'html'
            message.send()
            # TODO: SEND CONFIRMATION MAIL TO ADMIN
            message1 = EmailMessage(
                subject = f"New User SignUp Notification",
                body = f'Hello Admin,\n\n{username.capitalize()} just signed up on your website.\n\nRegards,\nDevTeam',
                from_email = 'admin@gmail.com',
                to = ['admin@gmail.com'],
            )
            message1.send()

            # LOGIC IF USER REGISTERS VIA A REFERRAL LINK
            if referral_id is not None:
                recommended_by_user = Referral.objects.get(id=referral_id)
                instance = form.save()
                registered_user = userModel.objects.get(id=instance.id)
                registered_profile = Referral.objects.get(user=registered_user)
                registered_profile.recommended_by = recommended_by_user.user
                percent = (referral.bonus_percent / referral.bonus_amount) * referral.bonus_amount
                referral.bonus = F('bonus') + percent
                registered_profile.save()
                # UPDATE USER'S BALANCE
                # referral.user.balance = F('balance') + referral.bonus
                # referral.user.save()
                referral.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, (f"Account created for <b>{user.username.capitalize()}</b>.\
                    \nComplete your profile to gain full access to our services."))
                return redirect('dashboard:profile') 
            # LOGIC IF USER REGISTERS DIRECTLY
            else:
                form.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, (f"Account created for <b>{user.username.capitalize()}</b>.\
                    \nComplete your profile to gain full access to our services."))
                return redirect('dashboard:profile')   
    else:
        form = NewUserForm()
    return render(request, 'account/signup.html', {'form': form})
    

@user_not_authenticated
def login_request(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, (f"Hello <b>{user.username}</b>! You have been logged in."))
                return redirect('dashboard:dashboard')
    else:
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'account/login.html', context)


@login_required(login_url='account:login')
def security(request):
    if request.method == 'POST':
        form = PasswordChange(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            # TODO: SEND CONFIRMATION MAIL TO USER
            name = request.user.username
            context = ({
                'user': name,
            })
            html_version = './account/mails/password_change.html'
            html_message = render_to_string(html_version, context)
            subject = 'beeLabbs - Password Change Notification'
            message = EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
            message.content_subtype = 'html'
            message.send()
            messages.success(request, _("Your password was successfully updated!"))
            return redirect('dashboard:profile')
    else:
        form = PasswordChange(request.user)
    context = {
        'form': form
    }
    return render(request, 'account/security.html', context)
