# Generated by Django 4.2.7 on 2023-11-15 12:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_transaction_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date_create',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 15, 15, 58, 49, 501362)),
        ),
    ]
