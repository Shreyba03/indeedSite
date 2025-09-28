from django.contrib import admin
from .models import Job, Profile, Skill, Experience

# Register your models here.
admin.site.register(Job)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'headline')
    search_fields = ('user__username', 'headline', 'skills')
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Skill)
admin.site.register(Experience)
