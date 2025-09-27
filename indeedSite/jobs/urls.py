from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='jobs.index'),
    path('<int:id>/', views.show, name='jobs.show'),
    path('profile/<int:user_id>/', views.profile, name='profile.index'),
    path('edit_profile/<int:user_id>/', views.edit_profile, name='profile.edit'),
]