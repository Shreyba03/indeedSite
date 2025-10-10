from django.urls import path
from . import views

'''
urlpatterns = [
    path('', views.index, name='jobs.index'),
    path('<int:id>/', views.show, name='jobs.show'),
    path('<int:job_id>/apply/', views.apply_to_job, name='jobs.apply'),
    path('profile/<int:user_id>/', views.profile, name='profile.index'),
    path('profile/<int:user_id>/edit/', views.edit_profile, name='profile.edit'),
    path('profile/<int:user_id>/skills/edit/', views.edit_skills, name='skills.edit'),
    path('profile/<int:user_id>/experience/edit/', views.edit_experience, name='experience.edit'),
]
'''

urlpatterns = [
    path("", views.job_list, name="job_list"),
    path("<int:id>/", views.job_detail, name="job_detail"),
    path('profile/<int:user_id>/', views.profile, name='profile.index'),
    path('profile/<int:user_id>/edit/', views.edit_profile, name='profile.edit'),
    path('profile/<int:user_id>/skills/edit/', views.edit_skills, name='skills.edit'),
    path('profile/<int:user_id>/experience/edit/', views.edit_experience, name='experience.edit'),
    path("<int:id>/apply/", views.apply_to_job, name="apply_to_job"),
    path("applications/", views.my_applications, name="my_applications"),
    path('recommended/', views.recommended_jobs, name='recommended_jobs'),
    path("map/", views.job_map_page, name="job_map_page"),
    path("map-data/", views.job_map_data, name="job_map_data"), 
    path("create-job/", views.create_job, name="job.create"), 
    #path("user-list/", views.list_users, name="job.users"), 
]