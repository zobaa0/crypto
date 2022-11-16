from celery import shared_task


@shared_task
def activate_subscription(instance_id):
    """
    Task to automatically calculate and add daily profit
    to each user with an active plan.
    """
    # GLOBAL IMPORTS
    from dashboard.models import Subscription
    from django.db.models import F
    import time as t

    # GET THE SUBSCRIPTION INSTANCE
    instance = Subscription.objects.get(pk=instance_id)
    user=instance.user

    # CALC VARIABLES
    percent = (instance.plan.percent / instance.plan.calc_percent) * instance.sub_amount
    profit_gained = (instance.plan.percent / instance.plan.calc_percent) * instance.sub_amount

    # BASIC PLAN
    if instance.plan.plan_name == "Basic":
        timer = 0
        while timer <= 172800:
            timer +=1 
            t.sleep(1)
            if timer == 86400:
                user.balance = F('balance') + percent
                user.profit = F('profit') + profit_gained
                user.save()
            if timer == 172800:
                user.balance = F('balance') + percent + instance.sub_amount
                user.profit = F('profit') + profit_gained
                user.save()
                Subscription.objects.filter(pk=instance_id).update(
                    status = 'Expired',
                )
                # instance.status = 'Expired'
                # instance.active = False
                # instance.save()
                break
        return "Done"
    # GOLD PLAN
    if instance.plan.plan_name == "Gold":
        timer = 0
        while timer <= 172800:
            timer +=1 
            t.sleep(1)
            if timer == 86400:
                user.balance = F('balance') + percent
                user.profit = F('profit') + profit_gained
                user.save()
            if timer == 172800:
                user.balance = F('balance') + percent + instance.sub_amount
                user.profit = F('profit') + profit_gained
                user.save()
                Subscription.objects.filter(pk=instance_id).update(
                    status = 'Expired',
                )
                break
        return 'Done'
    # PLATINUM PLAN
    if instance.plan.plan_name == "Platinum":
        timer = 0
        while timer <= 172800:
            timer +=1 
            t.sleep(1)
            if timer == 86400:
                user.balance = F('balance') + percent
                user.profit = F('profit') + profit_gained
                user.save()
            if timer == 172800:
                user.balance = F('balance') + percent + instance.sub_amount
                user.profit = F('profit') + profit_gained
                user.save()
                Subscription.objects.filter(pk=instance_id).update(
                    status = 'Expired',
                )
                break
        return 'Done'


# @shared_task
# def deactivate_subscription():
#     from dashboard.models import Subscription
#     import datetime as dt
#     now = dt.date.today()
#     Subscription.objects.filter(expires_at__lt=now).update(
#         active = False,
#         status = "Expired",
#     )

"""
TODO: COMMANDS TO RUN CELERY
1. celery -A crypto worker -l debug
2. celery -A crypto flower
3. celery -A crypto --pool=solo -l info
4. celery -A crypto worker -l info --concurrency=2 --without-gossip --pool=solo   #> Only one process can run at a time, hence solo.
4. celery -A crypto worker -l info --concurrency=20 --without-gossip --pool=gevent   #> Multiple processes can run simultaneously, hence gevent.
5. When a user subscribes via account balance. The account automatically deduct the deposit amount from the current balance. Meaning: the user
    automatically looses the initial amount deposit. Which might not be so initially. Ask how the account balance should be structured and
    restructure the code accordingly. Same applies when a user subscribes via 'Wallet'.
"""
    