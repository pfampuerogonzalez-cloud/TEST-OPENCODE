from django import forms
from .models import Course, Subject, Grade, Attendance


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["nombre", "descripcion", "año"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["nombre", "codigo", "descripcion", "profesores", "cursos"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "profesores": forms.CheckboxSelectMultiple,
            "cursos": forms.CheckboxSelectMultiple,
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["student", "subject", "valor", "tipo_nota", "fecha", "observacion"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "observacion": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, course=None, teacher=None, **kwargs):
        super().__init__(*args, **kwargs)
        if course:
            self.fields["student"].queryset = course.alumnos.all()
        if teacher:
            self.fields["subject"].queryset = teacher.subjects.all()


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["student", "course", "subject", "fecha", "estado", "observacion"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "observacion": forms.Textarea(attrs={"rows": 2}),
        }
