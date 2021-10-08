from django.shortcuts import render, redirect
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,

)
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def register_user_view(request):
    if request.method == 'POST':
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'User created successfully!')
            return redirect('companies:home')
    else:
        register_form = UserCreationForm()

    context = {
        'register_form': register_form,
    }
    return render(request, 'registration/register.html', context=context)


def login_user_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in!!')
                return redirect('companies:home')
            else:
                messages.error(request, 'Wrong username/password!')
                return redirect('members:login_user')
    else:
        login_form = AuthenticationForm()

    context = {
        'login_form': login_form,
    }
    return render(request, 'registration/login.html', context=context)


def logout_user_view(request):
    logout(request)
    messages.success(request, 'Logged out!')
    return redirect('members:login_user')



