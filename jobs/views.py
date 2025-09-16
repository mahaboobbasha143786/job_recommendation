from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job
from .forms import JobForm, SignUpForm
from django.contrib.auth import login
from django.db import models
from django.contrib import messages

# Homepage view
def index(request):
    jobs = Job.objects.all()
    return render(request, "jobs/index.html", {"jobs": jobs})

# Signup view
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = SignUpForm()
    return render(request, "jobs/signup.html", {"form": form})

# Post job view
@login_required
def post_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect("index")
    else:
        form = JobForm()
    return render(request, "jobs/post_job.html", {"form": form})


# Job detail view
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, "jobs/job_detail.html", {"job": job})

# Save a job
@login_required
def save_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.user in job.saved_by.all():
        job.saved_by.remove(request.user)  # Unsave if already saved
    else:
        job.saved_by.add(request.user)  # Save job
    return redirect("saved_jobs")

# View saved jobs
@login_required
def saved_jobs(request):
    jobs = Job.objects.filter(saved_by=request.user)
    return render(request, "jobs/saved_jobs.html", {"jobs": jobs})

# Profile view
@login_required
def profile_view(request):
    saved = Job.objects.filter(saved_by=request.user)
    posted = Job.objects.all()  # Optional: filter by posted_by if you add that
    return render(request, "jobs/profile.html", {"saved_jobs": saved, "posted_jobs": posted})

# Search jobs
def search_jobs(request):
    query = request.GET.get('q', '')  # Get the search query from URL
    if query:
        # Search by title, company, skills, or location
        jobs = Job.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(company__icontains=query) |
            models.Q(skills_required__icontains=query) |
            models.Q(location__icontains=query)
        )
    else:
        jobs = Job.objects.all()
    
    context = {'jobs': jobs, 'query': query}
    return render(request, 'jobs/search_results.html', context)
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Optionally, save that the user applied if you want
    # e.g., job.applied_by.add(request.user) if you have a ManyToManyField
    
    # Redirect to the job detail or any confirmation page
    return redirect("job_detail", job_id=job.id)
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Job

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Only allow deletion if the current user is the poster
    if job.posted_by and job.posted_by != request.user:
        return HttpResponseForbidden("You are not allowed to delete this job.")
    
    job.delete()
    return redirect("profile")  # Redirect to profile after deletion
