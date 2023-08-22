from django.db import models


class ProjectManager(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    manager = models.ForeignKey(ProjectManager, on_delete=models.PROTECT, null=True)

    PROJECT_STATUS = (
        ('NS', 'Not started'),
        ('IP', 'In Progress'),
        ('CO', 'Completed'),
        ('CA', 'Cancelled'),
    )

    status = models.CharField(
        max_length=2, 
        choices=PROJECT_STATUS, 
        default='NS',
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    due_date = models.DateField()

    TASK_STATUS = (
        ('NS', 'Not started'),
        ('IP', 'In Progress'),
        ('CO', 'Completed'),
        ('CA', 'Cancelled'),
    )

    status = models.CharField(
        max_length=2, 
        choices=TASK_STATUS, 
        default='NS',
    )
    
    person_assigned = models.CharField(max_length=100)
    additional_information = models.TextField(null=True, blank=True)

    PRIORITIES = (
        ('H', 'high'),
        ('M', 'medium'),
        ('L', 'low'),
    )

    priority = models.CharField(
        max_length=1, 
        choices=PRIORITIES, 
        default='M',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["due_date"]
