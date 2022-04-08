from django.contrib import admin
from projects.models import Project, Assignment, Task, Milestone

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'state', 'sync')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Milestone)
admin.site.register(Task)
admin.site.register(Assignment)
