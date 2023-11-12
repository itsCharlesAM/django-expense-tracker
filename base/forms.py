from django.forms import ModelForm
from .models import Transaction


class transaction_form(ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
