from django.forms import ModelForm, DateInput
from .models import Task
from django.core.exceptions import ValidationError
import datetime

class TaskForm(ModelForm):
    class Meta:
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

        widgets = {
        'due_date': DateInput(format=('%m/%d/%Y'), attrs={'type':'date'}),
            }

    def clean_due_date(self):
        data = self.cleaned_data['due_date']
        if data < datetime.date.today():
            raise ValidationError('Invalid date - due date in past')
        return data
