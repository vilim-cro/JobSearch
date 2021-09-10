from django.db import models

class Job(models.Model):
    jobtitle = models.CharField(max_length=50)
    location = models.CharField(max_length=30)
    description = models.CharField(max_length=69420)
    about = models.CharField(max_length=69420)

    def __str__(self):
        return self.jobtitle


