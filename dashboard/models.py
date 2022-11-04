from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from datetime import datetime, date, timedelta
from django.utils import timezone
from django.db.models import F
import re
import time as t 
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from crypto import settings

# Custom user
user = get_user_model()

# Define today
today = date.today()

class Plan(models.Model):
    SUB_PLAN = (
        ('Basic', 'Basic Plan'),
        ('Gold', 'Gold Plan'),
        ('Platinum', 'Platinum Plan')
    )
    plan_name = models.CharField(max_length=8, choices=SUB_PLAN)
    percent = models.PositiveIntegerField()
    ref_bonus = models.PositiveIntegerField(default=10)
    min = models.DecimalField(max_digits=10, decimal_places=2)
    max = models.DecimalField(max_digits=10, decimal_places=2)
    calc_percent = models.DecimalField(max_digits=10, editable=False, decimal_places=2, default=100.00, verbose_name='Percentage Formula')
    duration = models.PositiveIntegerField()

    def __str__(self):
        return self.plan_name

    # class Meta:
    #     ordering = ['plan_name']

class Subscription(models.Model):
    SUB_METHOD = (
        ('Account', 'Account Balance'),
        ('Wallet', 'Wallet')
    )
    SUB_CURRENCY = (
        ('Btc', 'Bitcoin - BTC'),
        ('Eth', 'Ethereum - ETH'),
        ('Trc20', 'Tether - USDT(TRC20)')
    )
    SUB_STATUS =(
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Expired', 'Expired')
    ) 
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="user")
    type = models.CharField(max_length=10, default="Deposit", editable=False)
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING, related_name="plan")
    sub_method = models.CharField(max_length=24, choices=SUB_METHOD, default='Account')
    sub_currency = models.CharField(max_length=12, choices=SUB_CURRENCY, default='Btc')
    sub_amount = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    active_deposit = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    expires_at = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=9, choices=SUB_STATUS, default="Pending")
    verified_on = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=False)
    initiated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Username: {self.user.username.capitalize()} || Plan: {self.plan.plan_name}\
             || Status: {self.status} || Balance: ${self.user.balance}"

    def clean(self):
        """SUBSCRIPTION CUSTOM VALIDATION"""
        # Don't allow amount out of the Basic plan range
        if self.plan.plan_name == "Basic":
            if self.sub_amount < self.plan.min or self.sub_amount > self.plan.max:
                raise ValidationError({'sub_amount': _(f"Enter an amount within the range of ${self.plan.min} and ${self.plan.max}")})
            # Validate Account Balance
            if self.sub_method == "Account":
                if self.sub_amount > self.user.balance:
                    raise ValidationError({'sub_amount': _(f"Insufficient balance. Kindly recharge via your wallet")})
        # Don't allow amount out of the Advanced plan range
        elif self.plan.plan_name == "Gold":
            if self.sub_amount < self.plan.min or self.sub_amount > self.plan.max:
                raise ValidationError({'sub_amount': _(f"Enter an amount within the range of ${self.plan.min} and ${self.plan.max}")})
            # Validate Account Balance
            if self.sub_method == "Account":
                if self.sub_amount > self.user.balance:
                    raise ValidationError({'sub_amount': _(f"Insufficient balance. Kindly recharge via your wallet")})
        # Don't allow amount out of the Platinum plan range
        else:
            if self.sub_amount < self.plan.min or self.sub_amount > self.plan.max:
                raise ValidationError({'sub_amount': _(f"Enter an amount within the range of ${self.plan.min} and ${self.plan.max}")})
            # Validate Account Balance
            if self.sub_method == "Account":
                if self.sub_amount > self.user.balance:
                    raise ValidationError({'sub_amount': _(f"Insufficient balance. Kindly recharge via your wallet")})

    @classmethod
    def update_subscription(cls, sender, instance, created, *args, **kwargs):
        """Update other optional subscription fields on active"""
        Subscription.objects.filter(active=True).update(
            status = "Confirmed", verified_on = timezone.now(),
            # TODO: Case-scenario where the user has multiple deposit plans
            # active_deposit = F('active_deposit') + instance.sub_amount,
            expires_at = date.today() + timedelta(days=instance.plan.duration)
        )

    @classmethod
    def update_active_bal(cls, sender, instance, created, *args, **kwargs):
        """Update user account bal. after payment confirmation"""
        user=instance.user
        if instance.active == True and instance.sub_method == "Wallet":
            user.balance = F('balance') + instance.sub_amount
            user.save()
        if instance.sub_method == "Account":
            user.balance = F('balance') - instance.sub_amount
            user.save()
            
            # print('user: ',user.balance, ' instance: ', instance.sub_amount)

    # @classmethod
    # def activate_subscription(cls, sender, instance, created, *args, **kwargs):
    #     """Start the countdown"""
    #     user=instance.user
    #     # User Percentage
    #     percent = (instance.plan.percent / instance.plan.calc_percent) * instance.sub_amount

        # while instance.active:
        #     if instance.plan.plan_name == "Basic":
        #         print("working")
        #         timer = 0
        #         while timer <= 172800:
        #             timer +=1 
        #             t.sleep(1)
        #             if timer == 86400:
        #                 user.balance = F('balance') + percent
        #                 user.profit = user.balance - instance.sub_deposit
        #                 user.save()
        #             if timer == 172800:
        #                 user.balance = F('balance') + percent
        #                 user.profit = user.balance - instance.sub_deposit
        #                 user.save()

    # @classmethod
    # def deactivate_subscription(cls, sender, instance, created, *args, **kwargs):
    #     """Delete user account after due date"""
    #     if instance.active:
    #         expires =  date.today()+timedelta(days=instance.plan.duration)
    #         while True:
    #             if expires < today:
    #                 print(f'Days left: {(instance.del_account_due_date - today).days}')
    #                 instance.active == False
    #                 instance.status == "Expired"
    #                 break
                
post_save.connect(Subscription.update_subscription, sender=Subscription)
# post_save.connect(Subscription.activate_subscription, sender=Subscription)
# post_save.connect(Subscription.deactivate_subscription, sender=Subscription)


class Wallet(models.Model):
    NETWORK = (
        ('Btc', 'Bitcoin - BTC'),
        ('Eth', 'Ethereum - ETH'),
        ('Trc20', 'Tether - USDT(TRC20)')
    )
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=NETWORK, default='Btc', verbose_name="Wallet name")
    address = models.CharField(max_length=60, verbose_name="Wallet address")

    class Meta:
        verbose_name_plural = 'Wallet Address'
        # unique_together = ('user', 'type')

    def __str__(self):
        return f"{self.get_type_display()} - {self.address}" 

    def clean(self):
        """WALLET ADDRESS CUSTOM VALIDATION"""
        if not self and not self.required:
            return None

        # BITCOIN WALLET
        if self.type == "Btc":
            if not self.address.startswith("1") and not self.address.startswith('3') and not self.address.startswith('bc1'):
                raise ValidationError({'address': _(f"Invalid Bitcoin address.")})
            if "\n" in self.address:
                raise ValidationError({'address': _(f"Multiple lines in the Bitcoin address.")})
            if " " in self.address:
                raise ValidationError({'address': _(f"Spaces in the Bitcoin address.")})
            if re.match(r"[a-zA-Z1-9]{27,35}$", self.address) is None:
                raise ValidationError({'address': _(f"Invalid Bitcoin address.")})
        # ETHEREUM WALLET
        elif self.type == "Eth":
            if not self.address.startswith('0x'):
                raise ValidationError({'address': _(f"Invalid Ethereum address.")})
            if len(self.address) != 42:
                raise ValidationError({'address': _(f"Invalid Ethereum address.")})
            if "\n" in self.address:
                raise ValidationError({'address': _(f"Multiple lines in the Ethereum address.")})
            if " " in self.address:
                raise ValidationError({'address': _(f"Spaces in the Ethereum address.")})
        # USDT WALLET
        else:
            if not self.address.startswith("T"):
                raise ValidationError({'address': _(f"Invalid USDT address.")})
            if len(self.address) != 34:
                raise ValidationError({'address': _(f"Invalid USDT address.")})
            if "\n" in self.address:
                raise ValidationError({'address': _(f"Multiple lines in the USDT address.")})
            if " " in self.address:
                raise ValidationError({'address': _(f"Spaces in the USDT address.")})


class Withdrawal(models.Model):
    WITHDRAW_STATUS = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed')
    ) 
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_DEFAULT, default="Btc", verbose_name="Withdrawal wallet")
    type = models.CharField(max_length=10, default="Withdrawal", editable=False)
    # min_withdraw = models.ForeignKey(Min_withdraw, on_delete=models.DO_NOTHING, default=0.00)
    # subscription = models.ForeignKey(Subscription, on_delete=models.DO_NOTHING, default=True)
    amount =models.DecimalField(max_digits=1000, decimal_places=2, default=0.00, verbose_name="Withdrawal amount")
    min_withdraw = models.DecimalField(max_digits=1000, decimal_places=2, default=80.00, verbose_name='Minimum withdrawal')
    status = models.CharField(max_length=12, choices=WITHDRAW_STATUS, default="Pending", verbose_name="Withdrawal status")
    verified_on = models.DateTimeField(blank=True, null=True)
    # active = models.BooleanField(default=False)
    initiated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Username: {self.user.username.capitalize()} || Status: {self.status} || Balance: {self.user.balance}"

    def clean(self):
        """WITHDRAWAL CUSTOM VALIDATION"""
        # if self.subscription.active == True:
        #     raise ValidationError({'amount': _(f"Withdrawal failed. You still have an active subscription.")})
        if self.amount > self.user.balance:
            raise ValidationError({'amount': _(f"Withdrawal failed. Insufficient balance.")})
        if self.amount < self.user.balance and self.amount < self.min_withdraw:
            raise ValidationError({'amount': _(f"Withdrawal failed. Minimum withdrawal amount is ${self.min_withdraw}")})

    @classmethod
    def verify_withdrawal(cls, sender, instance, created, *args, **kwargs):
        """Update withdrawal verification date"""
        Withdrawal.objects.filter(status="Confirmed").update(verified_on = timezone.now())

    @classmethod
    def confirm_withdrawal(cls, sender, instance, created, *args, **kwargs):
        """
        Update user account bal. after payment confirmation
        and send confirmation mail to the user
        """
        user=instance.user
        if instance.status == "Confirmed":
            user.balance = F('balance') - instance.amount
            user.save()
            # print(f"Congratulation {user.username}! Your withdrawal request has been confirmed. 
            # {instance.wallet.get_type_display()} - ${instance.amount}")
            # TODO: SEND CONFIRMATION MAIL TO USER
            context = ({
                'user': user.username,
                'amount': instance.amount,
                'wallet': instance.wallet.type,
                'address': instance.wallet.address
            })
            # html_version = './dashboard/mails/active_with.html'
            # html_message = render_to_string(html_version, context)
            # subject = 'beeLabbs - Withdrawal Approved'
            # message = EmailMessage(subject, html_message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
            # message.content_subtype = 'html'
            # message.send()
            
post_save.connect(Withdrawal.confirm_withdrawal, sender=Withdrawal)
post_save.connect(Withdrawal.verify_withdrawal, sender=Withdrawal)


"""
LIST OF TODO'S
1. Adding the option for a user not to withdraw till his plan expires. Works in the admin but fails in the views
2. Wallet address can't be deleted yet. Kinda proving a thorn in the flesh to implement.
3. Implement the logic of incrementing the user's balance by the daily percentage of the plan subscribed to and deactivate the plan when it expiries
4. I bet that's all I can remember for now
"""





























# get_email_sent(request,receiver=[],subject='',context = {},template='emails/progress.html') 

# '''
# from django.conf import settings
# from django.template.loader import render_to_string
# from django.core.mail import EmailMultiAlternatives
# from django.utils.html import strip_tags

# def function(request,**kwargs):
#    sender = settings.EMAIL_HOST_USER
#    receiver = kwargs['receiver']
#    subject = kwargs['subject']
#    context = kwargs['context']
#    html_content = render_to_string(kwargs['template'], context) # render with dynamic value
#    text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.
#    email = EmailMultiAlternatives(subject, text_content, sender, receiver)
#    email.attach_alternative(html_content, "text/html")
#    email.send(fail_silently=True)
#    return True
        










# @receiver(post_save, sender=Subscription)
# def update_subscription(sender, instance=None, created=False, **kwargs):
#     if not instance:
#         return
        
#     if not hasattr(instance, '_dirty'):
#         return

#     if instance.active and instance.sub_method == "Wallet":
#         instance.user.balance = F('balance') + instance.sub_amount

#     try:
#         instance._dirty = True
#         instance.user.save()
#         instance.save()
#     finally:
#         del instance._dirty
        # instance.save()
        # print('State: ', instance.state, ' Expiries: ', instance.expiries_at, ' Verified: ', instance.verified_on, ' Name: ', instance.user.username)
        # if instance.sub_method == "Wallet":
    # else: 
    #     pass
    #         instance.user.balance = F('balance') + instance.sub_amount
    #         instance.user.save()
    #     instance.state = "Confirmed"
    #     instance.expiries_at = datetime.now().date() + timedelta(days=instance.plan.duration)
    #     instance.del_account_due_date = timezone.now().date() + timedelta(days=instance.deactivation_duration)
    #     if instance.del_account_due_date < today:
    #         instance.delete()


    # if subscribe.active:
                #     user.balance = F('balance')  + amount
                #     subscribe.state = "Confirmed"
                #     subscribe.expiries_at = datetime.now().date() + timedelta(days=plan.duration)
                #     subscribe.save()