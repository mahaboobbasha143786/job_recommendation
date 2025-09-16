from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    skills_required = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    apply_link = models.URLField()
    saved_by = models.ManyToManyField(User, blank=True)  
    posted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="jobs_posted"
    )
    # jobs/models.py
    applied_by = models.ManyToManyField(User, blank=True, related_name="applied_jobs")
# Users who saved this job

    def __str__(self):
        return f"{self.title} at {self.company}"
