# Generated by Django 4.1.4 on 2023-05-05 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usercredit', '0026_rename_commission_transaction_profit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='charges',
            new_name='deposit_charges',
        ),
        migrations.AddField(
            model_name='transaction',
            name='withdraw_charges',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]