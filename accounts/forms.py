from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Student, Teacher, AdminProfile
from academics.models import Course


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario", widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={"class": "form-control"}))


class StudentCreateForm(forms.ModelForm):
    username = forms.CharField(label="Nombre de usuario", max_length=150)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name = forms.CharField(label="Apellido", max_length=150)
    email = forms.EmailField(label="Email", required=False)
    courses = forms.ModelMultipleChoiceField(
        label="Cursos",
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Student
        fields = ["rut", "fecha_nacimiento", "telefono", "direccion"]
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
        }

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            email=self.cleaned_data.get("email", ""),
        )
        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()
            student.courses.set(self.cleaned_data["courses"])
        return student


class TeacherCreateForm(forms.ModelForm):
    username = forms.CharField(label="Nombre de usuario", max_length=150)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name = forms.CharField(label="Apellido", max_length=150)
    email = forms.EmailField(label="Email", required=False)

    class Meta:
        model = Teacher
        fields = ["rut", "telefono", "fecha_contrato", "especialidad"]
        widgets = {
            "fecha_contrato": forms.DateInput(attrs={"type": "date"}),
        }

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            email=self.cleaned_data.get("email", ""),
        )
        teacher = super().save(commit=False)
        teacher.user = user
        if commit:
            teacher.save()
        return teacher
