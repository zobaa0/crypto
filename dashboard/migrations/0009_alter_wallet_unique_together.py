# Generated by Django 4.1.1 on 2022-11-02 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_alter_wallet_user'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wallet',
            unique_together=set(),
        ),
    ]
