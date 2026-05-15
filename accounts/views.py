from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Student, Teacher
from .decorators import admin_required
from .forms import StudentCreateForm, TeacherCreateForm
from django.utils.decorators import method_decorator
from academics.models import Grade, Attendance, Course
from tasks_app.models import Task


@login_required
def dashboard(request):
    ctx = {}
    if hasattr(request.user, "student"):
        student = request.user.student
        ctx["courses"] = student.courses.all()
        ctx["recent_grades"] = Grade.objects.filter(student=student)[:10]
        ctx["pending_tasks"] = Task.objects.filter(course__in=student.courses.all()).order_by("fecha_entrega")[:10]
        ctx["role"] = "student"
    elif hasattr(request.user, "teacher"):
        teacher = request.user.teacher
        ctx["subjects"] = teacher.subjects.all()
        ctx["recent_grades"] = Grade.objects.filter(teacher=teacher)[:10]
        ctx["my_tasks"] = Task.objects.filter(teacher=teacher)[:10]
        ctx["role"] = "teacher"
    elif hasattr(request.user, "adminprofile") or request.user.is_superuser:
        ctx["total_students"] = Student.objects.count()
        ctx["total_teachers"] = Teacher.objects.count()
        ctx["total_courses"] = Course.objects.count()
        ctx["recent_grades"] = Grade.objects.all()[:10]
        ctx["role"] = "admin"
    return render(request, "dashboard.html", ctx)


@method_decorator(admin_required, name="dispatch")
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "accounts/student_list.html"
    context_object_name = "students"


@method_decorator(admin_required, name="dispatch")
class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentCreateForm
    template_name = "accounts/student_form.html"
    success_url = reverse_lazy("accounts:student_list")


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "accounts/student_detail.html"
    context_object_name = "student"

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        if pk:
            return Student.objects.get(pk=pk)
        return self.request.user.student


@method_decorator(admin_required, name="dispatch")
class TeacherListView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = "accounts/teacher_list.html"
    context_object_name = "teachers"


@method_decorator(admin_required, name="dispatch")
class TeacherCreateView(LoginRequiredMixin, CreateView):
    model = Teacher
    form_class = TeacherCreateForm
    template_name = "accounts/teacher_form.html"
    success_url = reverse_lazy("accounts:teacher_list")


class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = "accounts/teacher_detail.html"
    context_object_name = "teacher"

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        if pk:
            return Teacher.objects.get(pk=pk)
        return self.request.user.teacher
