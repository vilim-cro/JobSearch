from django.forms.widgets import PasswordInput
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from jobs.models import Job
from django.core import serializers

class NewUser(forms.Form):
    username = forms.CharField(max_length=16, label="Username: ", help_text="Up to 16 characters", widget=forms.TextInput(attrs={'class' : 'form-control'}))
    first_name = forms.CharField(max_length=16, label="First Name: ", help_text="Up to 16 characters", widget=forms.TextInput(attrs={'class' : 'form-control'}))
    last_name = forms.CharField(max_length=16, label="Last Name: ", help_text="Up to 16 characters", widget=forms.TextInput(attrs={'class' : 'form-control'}))
    email = forms.EmailField(max_length=64, label="Email: ", required = False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(max_length=16, label="Password: ", widget=PasswordInput(attrs={'class' : 'form-control'}))

# Returns the template with some user information
def index(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'You need to login first.')
        return HttpResponseRedirect(reverse('users:login'))

    return render(request, 'users/profile.html', {
        "user": request.user,
        "number_of_posts": len(request.user.job_posts.all())
    })

# If the user is authenticated, redirects to 'users/index.html', if not message is showed
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
                username = form.cleaned_data["username"],
                first_name = form.cleaned_data["first_name"],
                last_name = form.cleaned_data["last_name"],
                email = form.cleaned_data["email"],
                password = form.cleaned_data["password"])
            user.save()
            messages.add_message(request, messages.SUCCESS, 'User created! Now go to the login page and login.')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid form info')

    return render(request, 'users/register.html', {
        "form": NewUser
    })

def myposts(request):
    if request.user.is_authenticated:
        return render(request, 'users/myposts.html')
    return HttpResponseRedirect(reverse('users:login'))

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'You have been logged out.')
    return render(request, 'users/login.html')

# Deletes the job post if the authenticated user is also the job post creator
def delete(request, job_id):
    if request.user.is_authenticated and request.user == Job.objects.get(pk=job_id).creator:
        model = Job.objects.get(pk=job_id)
        model.delete()
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:myposts'))
    return HttpResponseRedirect(reverse('users:login'))

# Returns JSON job posts that were created by authenticated user
def myjobs(request):
    return HttpResponse(serializers.serialize('json', request.user.job_posts.all()), content_type = 'application/json')
    
