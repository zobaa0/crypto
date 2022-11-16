from .models import Subscription
from .models import Withdrawal
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime as dt
from django.utils import timezone


@receiver(post_save, sender=Subscription)
def update_subscription(sender, instance, *args, **kwargs):
    if instance.active == True:
        Subscription.objects.filter(id=instance.id).update(
            status = "Confirmed", verified_on = timezone.now(),
            # TODO: Case-scenario where the user has multiple deposit plans
            expires_at = dt.date.today() + dt.timedelta(days=instance.plan.duration),
        )

@receiver(post_save, sender=Withdrawal)
def verify_withdrawal(sender, instance, *args, **kwargs):
    if instance.status == 'Confirmed':
        Withdrawal.objects.filter(pk=instance.pk).update(
            verified_on = timezone.now(),
        )