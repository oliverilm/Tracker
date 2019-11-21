from django.contrib import admin

# Register your models here.
from Tracker.models import Project, CheckIn, UserInProject


class ProjectsAdmin(admin.ModelAdmin):
    count = UserInProject.objects.filter()
    list_display = ("name", "has_ended")

class CheckInAdmin(admin.ModelAdmin):
    list_filter = ("user", "project", "is_active")
    list_display = ("user", "project", "start", "stop", "is_active", "total_hours")

class UserInProjectAdmin(admin.ModelAdmin):
    list_display = ("user", "project")

admin.site.register(Project, ProjectsAdmin)
admin.site.register(CheckIn, CheckInAdmin)
admin.site.register(UserInProject, UserInProjectAdmin)