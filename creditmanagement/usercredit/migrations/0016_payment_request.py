# Generated by Django 4.1.4 on 2023-04-26 12:14

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('usercredit', '0015_alter_card_due_amount_alter_card_due_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment_Request',
            fields=[
                ('request_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('due_amount', models.FloatField(blank=True, default=0, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('modified_at', models.DateTimeField(default=datetime.datetime.now)),
                ('card', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requested_card_id', to='usercredit.card')),
            ],
        ),
    ]