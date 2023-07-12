# Generated by Django 4.1.4 on 2023-04-26 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usercredit', '0014_transaction_charges_alter_transaction_paid_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='due_amount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
