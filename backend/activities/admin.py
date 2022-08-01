from django.contrib import admin
from activities.models import Activity

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'project', 'reward', 
                    'activity_type', 'status', 'sync')

admin.site.register(Activity, ActivityAdmin)
