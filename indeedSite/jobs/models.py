from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255, blank=True)
    #skills = models.TextField(blank=True, help_text="Comma-separated list of skills")
    education = models.TextField(blank=True)
    #experience = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank = True)

    # FOR MAP
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # LINKS
    portfolio = models.URLField(blank=True)
    github = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # PRIVACY OPTIONS
    show_email = models.BooleanField(default=False)
    show_phone = models.BooleanField(default=False)

    # IF PROFILE IS A RECRUITER
    is_recruiter = models.BooleanField(default=False)
    company = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='project_list')
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.position} at {self.company}"

class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skill_list')
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=20, choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert'),
    ], default='Intermediate')
    
    def __str__(self):
        return f"{self.name} ({self.proficiency})"

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experience_list')
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
  
    def __str__(self):
        return f"{self.position} at {self.company}"
    

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    remote = models.BooleanField(default=False)
    visa_sponsorship = models.BooleanField(default=False)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    skills_required = models.TextField(help_text="Comma-separated list of skills", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    remote_friendly = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} @ {self.company}"


class Application(models.Model):
    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("under-review", "Under Review"),
        ("interview", "Interview"),
        ("rejected", "Rejected"),
        ("accepted", "Accepted"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.job.title} ({self.status})"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

class Search(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_searches')
    name = models.CharField(max_length=255)
    search_term = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_run = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.recruiter.username} - {self.name}"

