from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path('', views.index, name='index'),
    path('post', views.post, name='post'),
    path('find', views.find, name='find'),
    path('<int:job_id>', views.job, name='job'),
]
