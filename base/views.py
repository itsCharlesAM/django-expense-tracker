from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Transaction
from .forms import transaction_form
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


def login_page(request):
    req_username = None
    req_password = None

    if request.method == 'POST':
        req_username = request.POST.get('username')
        req_password = request.POST.get('password')

        try:
            user = User.objects.get(username=req_username)
        except:
            messages.error(request, 'User does not exist')

    user = authenticate(request, username=req_username, password=req_password)

    if user is not None:
        # login method creates session in database and browser
        login(request, user)
        return redirect('transactions')
    else:
        messages.error(request, 'Invalid username or password')

    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


# this will restrict the all_transactions page
@login_required(login_url='login')
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


@login_required(login_url='login')
def add_transaction(request):
    form = transaction_form()

    if request.method == 'POST':
        form = transaction_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transactions')

    context = {'form': form}
    return render(request, 'transactions/transaction_form.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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
