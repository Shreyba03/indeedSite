import csv
from django.contrib import admin
from .models import Job, Profile, Skill, Experience, Application, Message
from django.http import HttpResponse

# Register your models here.
admin.site.register(Job)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'headline')
    search_fields = ('user__username', 'headline', 'skills')
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Skill)
admin.site.register(Experience)
admin.site.register(Message)


@admin.action(description='Export selected applications as CSV')
def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=applications.csv'
    writer = csv.writer(response)
    
    # Write header
    writer.writerow(['ID', 'User', 'Job', 'Status', 'Note', 'Applied At'])
    
    # Write data
    for app in queryset:
        writer.writerow([app.id, app.user.username, app.job.title, app.status, app.note, app.applied_at])
    
    return response

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "user", "status", "applied_at")
    list_filter = ("status", "applied_at")
    search_fields = ("job__title", "user__username")
    actions = [export_as_csv]