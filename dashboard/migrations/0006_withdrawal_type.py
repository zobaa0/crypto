# Generated by Django 4.1.1 on 2022-10-30 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_subscription_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawal',
            name='type',
            field=models.CharField(default='Withdrawal', editable=False, max_length=10),
        ),
    ]