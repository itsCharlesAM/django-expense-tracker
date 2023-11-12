from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Transaction
from .forms import transaction_form
# Create your views here.


def show_all_transactions(request):
    all_transactions = Transaction.objects.all().order_by('-date_create')
    transactions_context = {'all_transactions': all_transactions}
    return render(request, 'transactions/transactions.html', transactions_context)


def add_transaction(request):
    form = transaction_form()

    if request.method == 'POST':
        form = transaction_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transactions')

    context = {'form': form}
    return render(request, 'transactions/transaction_form.html', context)


def edit_transaction(request, id):
    transaction = Transaction.objects.get(id=id)
    form = transaction_form(instance=transaction)

    context = {'form': form}
    return render(request, 'transactions/transaction_form.html', context)


def home(request):

    return render(request, 'home.html')


def day(request):

    return render(request, 'day.html')
