from django.shortcuts import render
from django import forms
from jobs.models import Job
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

class NewJobPost(forms.Form):
    jobtitle = forms.CharField(label = "Job Title: ")
    location = forms.CharField(label = "Location: ")
    description = forms.CharField(label = "Job Description: ", widget = forms.Textarea())
    about = forms.CharField(label = "About the company: ", widget = forms.Textarea())

def index(request):
    return render(request, 'jobs/index.html')

def find(request):
    jobs = Job.objects.all()[:10]
    if "j" in request.GET.keys():
        j = request.GET["j"]
        l = request.GET["l"]
        jobs = Job.objects.filter(jobtitle__contains = j)
        jobs = Job.objects.filter(location__contains = l)
    return render(request, 'jobs/find.html', {
        "jobs": jobs
    })

def post(request):
    if request.method == "POST":
        form = NewJobPost(request.POST)
        if form.is_valid():
            job = Job(jobtitle = form.cleaned_data["jobtitle"], 
                    location = form.cleaned_data["location"],
                    description = form.cleaned_data["description"],
                    about = form.cleaned_data["about"]
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
