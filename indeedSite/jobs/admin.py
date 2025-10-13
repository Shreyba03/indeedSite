from django.contrib import admin
from .models import Job, Profile, Skill, Experience, Application, Message

# Register your models here.
admin.site.register(Job)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'headline')
    search_fields = ('user__username', 'headline', 'skills')
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Skill)
admin.site.register(Experience)
admin.site.register(Message)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "user", "status", "applied_at")
    list_filter = ("status", "applied_at")
    search_fields = ("job__title", "user__username")