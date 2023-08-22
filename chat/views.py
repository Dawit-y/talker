from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm
from django.contrib import messages
# Create your views here.


def lobby(request):
    return render(request, 'chat/lobby.html', {})

def login_form(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        try:
            user = User.objects.get(username = username)   
        except:
            messages.error(request, 'User doesnt exist')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else :
            messages.error(request, 'something went wrong')

    return render(request, 'chat/login.html', {})

def register(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, form.error_messages)
            print(form.error_messages)
            form = UserRegistrationForm()
    return render(request, 'chat/register.html', {'form' : form})


def logout_form(request):
    logout(request)
    return redirect('home')