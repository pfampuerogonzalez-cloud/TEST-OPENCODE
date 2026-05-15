from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from .models import Course, Subject, Grade, Attendance
from accounts.decorators import admin_required, admin_or_teacher_required, teacher_required
from .forms import CourseForm, SubjectForm, GradeForm, AttendanceForm
from django.utils.decorators import method_decorator


@method_decorator(admin_or_teacher_required, name="dispatch")
class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "academics/course_list.html"
    context_object_name = "courses"


@method_decorator(admin_required, name="dispatch")
class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "academics/course_form.html"
    success_url = reverse_lazy("academics:course_list")


@method_decorator(admin_required, name="dispatch")
class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "academics/course_form.html"
    success_url = reverse_lazy("academics:course_list")


@method_decorator(admin_required, name="dispatch")
class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = "academics/course_confirm_delete.html"
    success_url = reverse_lazy("academics:course_list")


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "academics/course_detail.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        course = self.object
        ctx["students"] = course.alumnos.all()
        ctx["subjects"] = course.subjects.all()
        if hasattr(self.request.user, "student"):
            ctx["grades"] = Grade.objects.filter(
                student=self.request.user.student, subject__in=course.subjects.all()
            )
        elif hasattr(self.request.user, "teacher"):
            ctx["grades"] = Grade.objects.filter(
                subject__in=self.request.user.teacher.subjects.all(),
                student__in=course.alumnos.all(),
            )
        else:
            ctx["grades"] = Grade.objects.filter(
                student__in=course.alumnos.all(),
            )
        return ctx


@method_decorator(admin_or_teacher_required, name="dispatch")
class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = "academics/subject_list.html"
    context_object_name = "subjects"


@method_decorator(admin_required, name="dispatch")
class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "academics/subject_form.html"
    success_url = reverse_lazy("academics:subject_list")


@method_decorator(admin_or_teacher_required, name="dispatch")
class GradeListView(LoginRequiredMixin, ListView):
    model = Grade
    template_name = "academics/grade_list.html"
    context_object_name = "grades"

    def get_queryset(self):
        qs = Grade.objects.all()
        if hasattr(self.request.user, "student"):
            qs = qs.filter(student=self.request.user.student)
        elif hasattr(self.request.user, "teacher"):
            qs = qs.filter(teacher=self.request.user.teacher)
        return qs


@method_decorator(admin_or_teacher_required, name="dispatch")
class GradeCreateView(LoginRequiredMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = "academics/grade_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        course_id = self.kwargs.get("course_id")
        if course_id:
            kwargs["course"] = get_object_or_404(Course, pk=course_id)
        if hasattr(self.request.user, "teacher"):
            kwargs["teacher"] = self.request.user.teacher
        return kwargs

    def form_valid(self, form):
        if hasattr(self.request.user, "teacher"):
            form.instance.teacher = self.request.user.teacher
        return super().form_valid(form)

    def get_success_url(self):
        course_id = self.kwargs.get("course_id")
        if course_id:
            return reverse("academics:course_detail", kwargs={"pk": course_id})
        return reverse_lazy("academics:grade_list")


@method_decorator(admin_or_teacher_required, name="dispatch")
class GradeUpdateView(LoginRequiredMixin, UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = "academics/grade_form.html"
    success_url = reverse_lazy("academics:grade_list")


@method_decorator(admin_or_teacher_required, name="dispatch")
class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = "academics/attendance_list.html"
    context_object_name = "attendances"

    def get_queryset(self):
        qs = Attendance.objects.all()
        if hasattr(self.request.user, "student"):
            qs = qs.filter(student=self.request.user.student)
        return qs


@method_decorator(admin_or_teacher_required, name="dispatch")
class AttendanceCreateView(LoginRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = "academics/attendance_form.html"
    success_url = reverse_lazy("academics:attendance_list")

    def form_valid(self, form):
        if hasattr(self.request.user, "teacher"):
            form.instance.registered_by = self.request.user.teacher
        return super().form_valid(form)
