from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Transaction
from .forms import transaction_form
from django.contrib.auth.models import User as auth_user
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def login_page(request):
    req_username = None
    req_password = None

    if request.method == 'POST':
        req_username = request.POST.get('username').lower()
        req_password = request.POST.get('password')

        try:
            user = auth_user.objects.get(username=req_username)
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


def register_page(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            myUser = User.objects.create(
                username=user.username.lower(),
                password=user.password,
                balance=0, is_visible=True, date_create=datetime.now, date_update=None,
            )

            myUser.save()

            login(request, myUser)  # log in the registered user
            return redirect('transactions')
        else:
            messages.error(request, 'An error occured in user register')

    context = {'form': form}
    return render(request, 'register.html', context)


@login_required(login_url='login')
def user_profile(request, id):
    user = auth_user.objects.get(id=id)

    myUser = User.objects.get(user_ptr_id=id)
    context = {'user': user, 'myUser': myUser}
    return render(request, 'profile.html', context)


# this will restrict the all_transactions page
@login_required(login_url='login')
def show_all_transactions(request):

    search_req = request.GET.get(
        'search',
    )
    logged_user_id = request.user.id
    myUser = User.objects.get(user_ptr_id=logged_user_id)

    if str(search_req).__contains__("inc"):
        search_req = 1
    elif str(search_req).__contains__("ex"):
        search_req = 2

    if search_req is not None:  # search
        all_transactions = Transaction.objects.filter(
            Q(is_visible=True) & Q(user=logged_user_id) & (Q(amount__icontains=search_req) | Q(description__icontains=search_req)), ).order_by('-date_create')
    else:
        all_transactions = Transaction.objects.filter(
            Q(is_visible=True) & Q(user=logged_user_id)).order_by('-date_create')

    transactions_count = all_transactions.count()

    transactions_context = {
        'all_transactions': all_transactions, 'transactions_count': transactions_count, 'myUser': myUser}
    return render(request, 'index.html', transactions_context)


@login_required(login_url='login')
def add_transaction(request):
    logged_user = User.objects.filter(id=request.user.id).first()

    if request.method == 'POST':
        req_amount = request.POST.get('amount')
        req_description = request.POST.get('description')
        req_type = request.POST.get('type')

        if req_type == "1":
            logged_user.balance = logged_user.balance + int(req_amount)
        if req_type == "2":
            logged_user.balance = logged_user.balance - int(req_amount)

        logged_user.save()

        new_transaction = Transaction.objects.create(
            amount=req_amount, type=req_type, description=req_description, user=logged_user,
        )
        new_transaction.save()
        return redirect('index')

    return render(request, 'index.html')


@login_required(login_url='login')
def edit_transaction(request, id):
    user = User.objects.get(id=request.user.id)
    transaction = Transaction.objects.get(id=id)
    form = transaction_form(instance=transaction)

    if user.id != transaction.user.id:
        return HttpResponse('not owner')

    if request.method == 'POST':
        form = transaction_form(request.POST, instance=transaction)
        if form.is_valid():
            if transaction.type == 1:  # income
                user.balance = user.balance + transaction.amount
            if transaction.type == 2:  # expense
                user.balance = user.balance - transaction.amount

            transaction.date_update = datetime.now()
            user.date_update = datetime.now()
            user.save()
            form.save()
            return redirect('transactions')

    context = {'form': form}
    return render(request, 'transactions/transaction_form.html', context)


@login_required(login_url='login')
def delete_transaction(request, id):
    user = User.objects.get(id=request.user.id)

    transaction = Transaction.objects.get(id=id)

    if request.user.id != transaction.user.id:
        return HttpResponse('not owner')

    print(request)

    transaction.is_visible = False
    if transaction.type == 1:  # income
        user.balance = user.balance - transaction.amount
    if transaction.type == 2:  # expence
        user.balance = user.balance + transaction.amount

    user.save()
    transaction.save()
    return redirect('transactions')


def home(request):

    return render(request, 'home.html')


def day(request):

    return render(request, 'day.html')
