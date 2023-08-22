from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project, ProjectManager, Task
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .forms import TaskForm
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required


class ProjectListView(ListView):
    model = Project
    paginate_by = 7
        

class TaskListView(ListView):
    model = Task
    paginate_by = 7

    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs["project_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_name = Project.objects.get(id=self.kwargs["project_id"])
        project_id = self.kwargs["project_id"]
        context["project_name"] = project_name
        context["project_id"] = project_id
        return context


class ProjectManagerListView(ListView):
    model = ProjectManager
    paginate_by = 7


class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num_completed_tasks = Task.objects.filter(status='CO').filter(project_id=self.kwargs["pk"]).count()
        num_tasks = Task.objects.filter(project_id=self.kwargs["pk"]).count()
        if num_tasks:
            percent_completed_tasks = "{:.0%}".format(num_completed_tasks/num_tasks)
            context["percent_completed_tasks"] = percent_completed_tasks
        project_id = self.kwargs["pk"]
        context["project_id"] = project_id
        context["num_tasks"] = num_tasks
        context["num_completed_tasks"] = num_completed_tasks
        return context


class TaskDetailView(DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs["project_id"]
        task_id = self.kwargs["pk"]
        context["project_id"] = project_id
        context["task_id"] = task_id
        return context
    

class ProjectCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'projectmanagement_app.add_project'
    model = Project
    fields = [
        "name", 
        "description", 
        # "department", 
        "manager", 
        "status",
    ]

    def get_success_url(self):
        return reverse("index")

@login_required
@permission_required('projectmanagement_app.add_task', raise_exception=True)
def add_task(request, project_id):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('task-list', args=(project_id,)))
    else:
        form = TaskForm(initial={"project": project_id})

    context = {
            'form': form,
            'project_id': project_id,
        }

# 
    return render(request, "add_task.html", context)


class ProjectManagerCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'projectmanagement_app.add_projectmanager'
    model = ProjectManager
    fields = [
        "name", 
        "department",
    ]

    def get_success_url(self):
        return reverse("projectmanager-list")


class ProjectUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'projectmanagement_app.change_project'
    model = Project
    fields = [
        "name", 
        "description", 
        "department", 
        "manager", 
        "status",
    ]

    def get_success_url(self):
        return reverse("project-detail", args=[self.object.pk])


class TaskUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'projectmanagement_app.change_task'
    model = Task
    fields = [
        "project",
        "name",
        "due_date",
        "status",
        "person_assigned",
        "additional_information",
        "priority",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.object.project_id
        context["project_id"] = project_id
        return context

    def get_success_url(self):
        return reverse("task-list", args=[self.object.project_id])


class ProjectManagerUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'projectmanagement_app.change_projectmanager'
    model = ProjectManager
    fields = [
        "name", 
        "department",
    ]

    success_url = reverse_lazy('projectmanager-list')


class ProjectDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'projectmanagement_app.delete_project'
    model = Project
    success_url = reverse_lazy('index')


class TaskDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'projectmanagement_app.delete_task'
    model = Task
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs["project_id"]
        context["project_id"] = project_id
        return context

    def get_success_url(self):
        return reverse("task-list", args=[self.object.project_id])


class ProjectManagerDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'projectmanagement_app.delete_projectmanager'
    model = ProjectManager
    success_url = reverse_lazy('projectmanager-list')

    # check if there are any projects assigned to the manager, the manager cannot be deleted if there are some
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        number_assigned_projects = Project.objects.filter(manager=self.kwargs["pk"]).count()
        context["number_assigned_projects"] = number_assigned_projects
        return context


def statistics(request):
    num_projects = Project.objects.all().count()
    num_tasks = Task.objects.all().count()
    num_completed_tasks = Task.objects.filter(status='CO').count()
    try:
        percentage_completed_tasks = "{:.0%}".format(num_completed_tasks/num_tasks)
    except:
        percentage_completed_tasks = "0%"
    num_completed_projects = Project.objects.filter(status='CO').count()
    try:
        percentage_completed_projects = "{:.0%}".format(num_completed_projects/num_projects)
    except:
        percentage_completed_projects = "0%"

    context = {
        'num_projects': num_projects,
        'num_tasks': num_tasks,
        'num_completed_tasks': num_completed_tasks,
        'percentage_completed_tasks': percentage_completed_tasks,
        'num_completed_projects': num_completed_projects,
        'percentage_completed_projects': percentage_completed_projects,
    }

    return render(request, 'statistics.html', context=context)


def managers_projects(request, manager_id):
    projects = Project.objects.filter(manager=manager_id)
    manager_name = ProjectManager.objects.get(id=manager_id)
    context = {
        'projects': projects,
        'manager_id': manager_id,
        'manager_name': manager_name,
    }
    return render(request, 'managers_projects.html', context=context)


def custom_error_403(request, exception):
    return render(request, '403.html', {})

def custom_error_404(request, exception):
    return render(request, '404.html', {})