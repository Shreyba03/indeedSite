from django.urls import path
from . import views

urlpatterns = [
    path("", views.job_list, name="job_list"),
    path("<int:id>/", views.job_detail, name="job_detail"),                             # Provides more info about the job
    path('profile/<int:user_id>/', views.profile, name='profile.index'),
    path('profile/<int:user_id>/edit/', views.edit_profile, name='profile.edit'),
    path('profile/<int:user_id>/skills/edit/', views.edit_skills, name='skills.edit'),
    path('profile/<int:user_id>/experience/edit/', views.edit_experience, name='experience.edit'),
    path("<int:id>/apply/", views.apply_to_job, name="apply_to_job"),
    path("applications/", views.my_applications, name="my_applications"),
    path('recommended/', views.recommended_jobs, name='recommended_jobs'),              # Recommends jobs to users
    path("map/", views.job_map_page, name="job_map_page"),                              # Renders the page
    path("map-data/", views.job_map_data, name="job_map_data"),                         # Processes map data
    path("create-job/", views.create_job, name="job.create"),                           # Creates a job
    path("user-list/", views.user_list, name="job.users"),                              # User list
    path("inbox/<str:username>/", views.inbox, name="job_inbox"),                       # Message inbox, kinda like discord
    path("inbox/<str:username>/<int:id>/", views.deleteMsg, name="job_delete_msg"),     # Deletes messages
    path("<int:id>/recommended-users/", views.recommended_users, name="recommended_users"), # Recommends users to recruiters
    path('recruiter_pipeline/', views.recruiter_pipeline, name='recruiter_pipeline'),
    path('recruiter_pipeline/update/<int:app_id>/', views.update_application_status, name='update_application_status'),
    path('export/applications/', views.export_applications_csv, name='export_applications_csv'),
]