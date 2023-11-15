from django.forms import ModelForm
from .models import Transaction


class transaction_form(ModelForm):
    class Meta:
        model = Transaction
        exclude = ['user_id', 'date_create', 'date_update', 'is_visible']
