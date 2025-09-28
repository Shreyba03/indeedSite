from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='jobs.index'),
    path('<int:id>/', views.show, name='jobs.show'),
    path('<int:job_id>/apply/', views.apply_to_job, name='jobs.apply'),
    path('profile/<int:user_id>/', views.profile, name='profile.index'),
    path('profile/<int:user_id>/edit/', views.edit_profile, name='profile.edit'),
    path('profile/<int:user_id>/skills/edit/', views.edit_skills, name='skills.edit'),
    path('profile/<int:user_id>/experience/edit/', views.edit_experience, name='experience.edit'),
]