import time
import json
from django.shortcuts import render
from django import forms
from django.urls.base import reverse
from jobs.models import Job
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers

class NewJobPost(forms.Form):
    jobtitle = forms.CharField(label = "Job Title: ", widget=forms.TextInput(attrs={'class' : 'form-control'}))
    location = forms.CharField(label = "Location: ", widget=forms.TextInput(attrs={'class' : 'form-control'}))
    description = forms.CharField(label = "Job Description: ", widget = forms.Textarea(attrs={'class' : 'form-control users_form-control'}))
    about = forms.CharField(label = "About the company: ", widget = forms.Textarea(attrs={'class' : 'form-control users_form-control'}))

def index(request):
    return render(request, 'jobs/index.html')

def find(request):
    return render(request, 'jobs/find.html')

def load(request):
    if "j" in request.GET.keys():
        j = request.GET["j"]
        l = request.GET["l"]
        jobs = Job.objects.filter(jobtitle__icontains = j, location__icontains = l)
    else:
        jobs = Job.objects.all()

    start = int(request.GET.get("start") or 0)
    end = int (request.GET.get("end") or start + 9)

    qs = jobs[start - 1:end]
    qs_json = serializers.serialize('json', qs)

    if start != 1:
        time.sleep(1)

    return HttpResponse(qs_json, content_type = 'application/json')

def post(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'To post a job offer you need to login/register first.')
        return HttpResponseRedirect(reverse('users:login'))

    if request.method == "POST":
        form = NewJobPost(request.POST)
        if form.is_valid():
            job = Job(jobtitle = form.cleaned_data["jobtitle"], 
                    location = form.cleaned_data["location"],
                    description = form.cleaned_data["description"],
                    about = form.cleaned_data["about"],
                    creator = request.user
                    )
            job.save()
        else:
            return render(request, 'jobs/post.html', {
                "form": form
    })
    return render(request, 'jobs/post.html', {
        "form": NewJobPost
    })

def job(request, job_id):
    job = Job.objects.get(pk = job_id)
    return render(request, 'jobs/job.html', {
        'job': job
    })
