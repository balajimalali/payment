# Generated by Django 4.1.1 on 2022-09-16 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_transaction_txn_id_pu'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='mode_err',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
