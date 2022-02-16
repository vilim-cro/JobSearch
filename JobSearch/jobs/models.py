from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    jobtitle = models.CharField(max_length=50)
    location = models.CharField(max_length=30)
    description = models.TextField(max_length=69420)
    about = models.TextField(max_length=69420)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_posts", default=1)

    def __str__(self):
        return self.jobtitle


