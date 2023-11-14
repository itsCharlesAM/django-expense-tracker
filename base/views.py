from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Transaction
from .forms import transaction_form
# Create your views here.


def show_all_transactions(request):
    search_req = request.GET.get(
        'search',
    )

    if str(search_req).__contains__("inc"):
        search_req = 1
    elif str(search_req).__contains__("ex"):
        search_req = 2

    if search_req is not None:  # search
        all_transactions = Transaction.objects.filter(
            Q(is_visible=True) & (Q(amount__icontains=search_req) | Q(description__icontains=search_req)), ).order_by('-date_create')
    else:
        all_transactions = Transaction.objects.filter(
            is_visible=True).order_by('-date_create')

    transactions_count = all_transactions.count()

    transactions_context = {
        'all_transactions': all_transactions, 'transactions_count': transactions_count}
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

    if request.method == 'POST':
        form = transaction_form(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transactions')

    context = {'form': form}
    return render(request, 'transactions/transaction_form.html', context)


def delete_transaction(request, id):
    transaction = Transaction.objects.get(id=id)
    if request.method == 'POST':
        transaction.is_visible = False
        transaction.save()
        return redirect('transactions')

    return render(request, 'transactions/delete.html', {'obj': transaction})


def home(request):

    return render(request, 'home.html')


def day(request):

    return render(request, 'day.html')
