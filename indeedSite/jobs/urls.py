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
    path("edit-job/<int:job_id>", views.edit_job, name="job.edit"),                           # Creates a job
    path("user-list/", views.user_list, name="job.users"),                              # User list
    path("inbox/<str:username>/", views.inbox, name="job_inbox"),                       # Message inbox, kinda like discord
    path("inbox/<str:username>/<int:id>/", views.deleteMsg, name="job_delete_msg"),     # Deletes messages
    path("<int:id>/recommended-users/", views.recommended_users, name="recommended_users"), # Recommends users to recruiters
    path('kanaban/', views.recruiter_pipeline, name='recruiter_pipeline'),
    path('kanaban/update/<int:app_id>/', views.update_application_status, name='update_application_status'),
    path('contact/<int:user_id>/', views.send_email, name='send_email'),
    path('notifications/', views.notifications, name="notificiations"),
    path('<int:job_id>/applicant-map/', views.applicant_map, name='applicant_map'),
    path('<int:job_id>/applicant-map-data/', views.applicant_map_data, name='applicant_map_data'),

]