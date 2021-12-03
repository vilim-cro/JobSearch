from django.forms.widgets import PasswordInput
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages


class NewUser(forms.Form):
    username = forms.CharField(max_length=16, label="Username: ", help_text="Up to 16 characters")
    email = forms.EmailField(max_length=64, label="Email: ", required = False)
    password = forms.CharField(max_length=16, label="Password: ", widget=PasswordInput)
    #cv = forms.FileField(label="Your CV: ", required=False)



def index(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'You need to login first.')
        return HttpResponseRedirect(reverse('users:login'))

    return render(request, 'users/profile.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('users:index'))
        else:
            messages.add_message(request, messages.ERROR, 'Invalid credentials')
    return render(request, 'users/login.html')

def register(request):
    if request.method == "POST":
        form = NewUser(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data["username"],
                form.cleaned_data["email"],
                form.cleaned_data["password"])
            user.save()
            messages.add_message(request, messages.SUCCESS, 'User created! Now go to the login page and login.')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid form info')

    return render(request, 'users/register.html', {
        "form": NewUser
    })

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'You have been logged out.')
    return render(request, 'users/login.html')
    
