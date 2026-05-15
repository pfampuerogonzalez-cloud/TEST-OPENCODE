from django import forms
from .models import Task, Submission


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["titulo", "descripcion", "subject", "course", "fecha_entrega", "archivo"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 4}),
            "fecha_entrega": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, teacher=None, **kwargs):
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields["subject"].queryset = teacher.subjects.all()


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["archivo", "comentario"]
        widgets = {
            "comentario": forms.Textarea(attrs={"rows": 3}),
        }


class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["nota", "feedback"]
        widgets = {
            "feedback": forms.Textarea(attrs={"rows": 3}),
        }
