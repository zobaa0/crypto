from django.http import BadHeaderError
from django.shortcuts import render, redirect
from .forms import NewUserForm, ResetPasswordForm, UserLoginForm, PasswordChange
from django.contrib.auth import get_user_model, login, authenticate, update_session_auth_hash
from django.contrib import messages
from main.decorators import user_not_authenticated
from .models import Referral
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from crypto import settings
from django.contrib.auth.decorators import login_required 
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

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
            subject = 'Welcome to Xandcoin'
            message = EmailMessage(subject, html_message, 'settings.EMAIL_HOST_USER', [email])
            message.content_subtype = 'html'
            message.send(fail_silently=True)
            # TODO: SEND CONFIRMATION MAIL TO ADMIN
            message1 = EmailMessage(
                subject = f"New User SignUp Notification",
                body = f'Hello Admin,\n\n{username.capitalize()} just signed up on your website.\n\nRegards,\nDevTeam',
                from_email = 'settings.EMAIL_HOST_USER',
                to = ['okonkwogodspower@yahoo.com'],
            )
            message1.send(fail_silently=True)

            # LOGIC IF USER REGISTERS VIA A REFERRAL LINK
            if referral_id is not None:
                recommended_by_user = Referral.objects.get(id=referral_id)
                instance = form.save()
                registered_user = userModel.objects.get(id=instance.id)
                registered_profile = Referral.objects.get(user=registered_user)
                registered_profile.recommended_by = recommended_by_user.user
                # percent = (referral.bonus_percent / referral.bonus_amount) * referral.bonus_amount
                # referral.bonus = F('bonus') + percent
                registered_profile.save()
                ### UPDATE USER'S BALANCE
                ### referral.user.balance = F('balance') + referral.bonus
                ### referral.user.save()
                # referral.save()
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
        valuenext = request.POST.get('next')
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, (f"Hello <b>{user.username}</b>! You have been logged in."))
                if valuenext == "":
                    return redirect('dashboard:dashboard')
                else:
                    return redirect(valuenext)
    else:
        form = UserLoginForm()
    context = {
        'form': form,
        # 'valuenext': valuenext
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
            subject = 'Xandcoin - Password Change Notification'
            message = EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [request.user.email])
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


@user_not_authenticated
def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = userModel.objects.filter(Q(email=user_email))
            if associated_user.exists():
                for user in associated_user:
                    context = ({
                        'user': user,
                        'domain': '13.40.240.230',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token':default_token_generator.make_token(user),
                        "protocol": 'https' if request.is_secure() else 'http',
                    })
                    html_version = './account/mails/password_reset.html'
                    html_message = render_to_string(html_version, context)
                    subject = 'Xandcoin - Password Reset Requested'
                    message = EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
                    message.content_subtype = 'html'
                try:
                    message.send()
                except BadHeaderError:
                    messages.error(request, ( "Problem sending reset password email, <b>SERVER PROBLEM</b>"))
                messages.success(request, ('A message with reset password instructions has been sent to the email provided.'))
            else:
                messages.success(request, ('A message with reset password instructions has been sent to the email provided.'))
    else:
        form = ResetPasswordForm()
    context = {
        'form': form
    }
    return render(request, 'account/password_reset.html', context)