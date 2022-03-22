from django.http import HttpResponseRedirect
from django.urls.base import reverse

def index(request):
    return HttpResponseRedirect(reverse('jobs:index'))