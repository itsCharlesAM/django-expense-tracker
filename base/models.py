from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class User(User):
    # id = models.BigAutoField(primary_key=True)
    # username = models.CharField(max_length=20, null=False)
    # first_name = models.CharField(max_length=20, null=False)
    # last_name = models.CharField(max_length=20, null=False)
    balance = models.FloatField(null=False, default=0)
    is_visible = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    amount = models.FloatField(null=False, default=0)

    class TransactionType(models.IntegerChoices):
        INCOME = 1, 'Income'
        EXPENSE = 2, 'Expense'
    type = models.IntegerField(choices=TransactionType.choices, null=True)

    description = models.TextField(null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_visible = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
