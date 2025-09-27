from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Job(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    salary = models.IntegerField()
    description = models.TextField()
    logo = models.ImageField(upload_to='job_images/', blank=True, null=True)
    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255, blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated list of skills")
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)

    # Toggleable links and info
    portfolio = models.URLField(blank=True)
    github = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"