from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render

# Create your views here.
from django import forms

from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.shortcuts import redirect
from faker import Faker

from todo.api import create_default_todo  # NOQA
from user.api import create_user  # NOQA

fake = Faker()


class RegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name', 'style': 'width: 300px;', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name', 'style': 'width: 300px;', 'class': 'form-control'}))
    email = forms.EmailField()


class BadRequestException(Exception):

    def __init__(self, msg):
        self.msg = msg


def _validate_data(username, password):
    error = None
    if not username:
        raise BadRequestException('Username is required')

    if not password:
        raise BadRequestException('Password is required')

    return error


def register_view(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')

    username = request.POST['username']
    password = request.POST['password']
    try:
        _validate_data(username, password)
    except BadRequestException as e:
        messages.add_message(request, messages.ERROR, e.msg)
        return render(request, 'user/register.html')
    user_exists = User.objects.filter(username=username).exists()
    if user_exists:
        messages.add_message(request, messages.ERROR, 'Username already exists')
        return render(request, 'user/register.html')

    # create user
    with transaction.atomic():
        user = create_user(username, fake.email(), password)
        create_default_todo(user)

    return redirect(reverse('auth:login'))


def login_view(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    username = request.POST['username']
    password = request.POST['password']
    try:
        _validate_data(username, password)
    except BadRequestException as e:
        messages.add_message(request, messages.ERROR, e.msg)
        return render(request, 'user/login.html')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # redirect to index view
        return redirect(reverse('todo:index'))
    else:
        messages.add_message(request, messages.ERROR, 'Username or password is incorrect')
        return render(request, 'user/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'user/login.html')
