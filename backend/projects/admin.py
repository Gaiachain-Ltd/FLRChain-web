from django.contrib import admin
from projects.models import Project, Assignment, Task, Milestone

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'state', 'sync')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Milestone)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'reward', 'count', 'finished', 'batch_paid')

admin.site.register(Task, TaskAdmin)
admin.site.register(Assignment)
