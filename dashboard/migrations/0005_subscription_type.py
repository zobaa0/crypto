# Generated by Django 4.1.1 on 2022-10-30 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_subscription_plan_alter_subscription_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='type',
            field=models.CharField(default='Deposit', editable=False, max_length=10),
        ),
    ]
