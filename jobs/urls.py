from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="jobs/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="index"), name="logout"),
    path("post-job/", views.post_job, name="post_job"),
    path("job/<int:job_id>/", views.job_detail, name="job_detail"),  # Add this
    path("save-job/<int:job_id>/", views.save_job, name="save_job"),
    path("saved-jobs/", views.saved_jobs, name="saved_jobs"),
    path("profile/", views.profile_view, name="profile"),
    path("search/", views.search_jobs, name="search_jobs"),
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("delete-job/<int:job_id>/", views.delete_job, name="delete_job"),

]
