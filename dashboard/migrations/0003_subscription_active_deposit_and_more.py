# Generated by Django 4.1.1 on 2022-10-30 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_subscription_sub_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='active_deposit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=1000),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='sub_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=1000),
        ),
    ]
