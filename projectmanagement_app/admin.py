from django.contrib import admin
from projectmanagement_app.models import Project, Task, ProjectManager

admin.site.register(Project)
admin.site.register(ProjectManager)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'person_assigned')
    list_filter = ('project_id',)
