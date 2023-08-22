from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="index"),
    path("project/<int:project_id>/tasks/", login_required(views.TaskListView.as_view()), name="task-list"),
    path("project/<int:project_id>/tasks/<int:pk>/", login_required(views.TaskDetailView.as_view()), name="task-detail"),
    path("project/<int:pk>/projectdetails/", login_required(views.ProjectDetailView.as_view()), name="project-detail"),
    path("projects/add/", views.ProjectCreate.as_view(), name="project-create"),
    path("project/<int:project_id>/tasks/add/", views.add_task, name="task-create"),
    path("managers/add/", views.ProjectManagerCreate.as_view(), name="projectmanager-create"),
    path("projects/<int:pk>/projectdetails/update/", views.ProjectUpdate.as_view(), name="project-update"),
    path("project/<int:project_id>/tasks/<int:pk>/update/", views.TaskUpdate.as_view(), name="task-update"),
    path("managers/<int:pk>/update", views.ProjectManagerUpdate.as_view(), name="projectmanager-update"),
    path("projects/<int:pk>/projectdetails/delete/", views.ProjectDelete.as_view(), name="project-delete"),
    path("project/<int:project_id>/tasks/<int:pk>/delete/", views.TaskDelete.as_view(), name="task-delete"),
    path("managers/<int:pk>/delete/", views.ProjectManagerDelete.as_view(), name="projectmanager-delete"),
    path("managers/", views.ProjectManagerListView.as_view(), name="projectmanager-list"),
    path("managers/<int:manager_id>/", login_required(views.managers_projects), name="managers-projects"),
    path("statistics/", login_required(views.statistics), name="statistics"),
]
