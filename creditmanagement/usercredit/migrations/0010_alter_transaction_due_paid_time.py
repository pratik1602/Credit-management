# Generated by Django 4.1.4 on 2023-04-20 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usercredit', '0009_remove_transaction_due_paid_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='due_paid_time',
            field=models.TimeField(),
        ),
    ]
