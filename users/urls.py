from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('myposts', views.myposts, name='myposts'),
    path('<int:job_id>', views.delete, name='delete'),
]
