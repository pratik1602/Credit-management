# Generated by Django 4.1.4 on 2023-04-13 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usercredit', '0003_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='credit_amount',
            field=models.FloatField(default=0),
        ),
    ]