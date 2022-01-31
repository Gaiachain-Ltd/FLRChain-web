from django.contrib import admin
from projects.models import Project, Assignment, Task, Milestone

admin.site.register(Project)
admin.site.register(Milestone)
admin.site.register(Task)
admin.site.register(Assignment)
