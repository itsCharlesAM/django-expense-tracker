# Generated by Django 4.2.7 on 2023-11-15 12:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_transaction_date_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date_create',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 15, 16, 1, 7, 448209)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date_update',
            field=models.DateTimeField(null=True),
        ),
    ]