from django.shortcuts import render
from django import forms
from jobs.models import Job
from django.http import HttpResponse, Http404
from django.forms.models import model_to_dict

class NewJobPost(forms.Form):
    jobtitle = forms.CharField(label = "Job Title: ")
    location = forms.CharField(label = "Location: ")
    description = forms.CharField(label = "Job Description: ", widget = forms.Textarea())
    about = forms.CharField(label = "About the company: ", widget = forms.Textarea())

class JobSearch(forms.Form):
    JobTitle = forms.CharField(
        label = "",
        required = False,
        widget = forms.TextInput(attrs={
            'class': 'form-control me-2',
            'id': 'jobtitle',
            'placeholder': 'Job Title, Keyword, Company...'
        }))
    Location = forms.CharField(
        label = "",
        required = False,
        widget = forms.TextInput(attrs={
            'class': 'form-control me-2',
            'id': 'location',
            'placeholder': 'Desired Location...'
        }))

def index(request):
    return render(request, 'jobs/index.html')

def find(request):
    if request.method == "POST":
        form = JobSearch(request.POST)
        if form.is_valid():
            jobtitle = form.cleaned_data["JobTitle"]
            location = form.cleaned_data["Location"]

            if jobtitle != "":
                if location != "":
                    return render(request, 'jobs/find.html', {
                        "form": JobSearch(),
                        "jobs": Job.objects.filter(jobtitle = jobtitle, location = location),
                    })
                return render(request, 'jobs/find.html', {
                    "form": JobSearch(),
                    "jobs": Job.objects.filter(jobtitle = jobtitle),
                })
            elif location != "":
                return render(request, 'jobs/find.html', {
                    "form": JobSearch(),
                    "jobs": Job.objects.filter(location = location),
                })

    jobs = []
    for job in Job.objects.all():
        jobs.append(model_to_dict(job))
    print(jobs)
    
    return render(request, 'jobs/find.html', {
        "form": JobSearch(),
        "jobs": Job.objects.all(),
        "mydata": {"jobs": jobs}
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
        "form": NewJobPost()
    })
