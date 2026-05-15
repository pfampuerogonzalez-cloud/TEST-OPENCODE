from datetime import date
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from .models import Task, Submission
from .forms import TaskForm, SubmissionForm, GradeSubmissionForm
from accounts.decorators import teacher_required, student_required, admin_or_teacher_required
from academics.models import Course
from django.utils.decorators import method_decorator


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks_app/task_list.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["today"] = date.today()
        return ctx

    def get_queryset(self):
        qs = Task.objects.all()
        if hasattr(self.request.user, "student"):
            student = self.request.user.student
            qs = qs.filter(course__in=student.courses.all())
        elif hasattr(self.request.user, "teacher"):
            qs = qs.filter(teacher=self.request.user.teacher)
        return qs


@method_decorator(admin_or_teacher_required, name="dispatch")
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks_app/task_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self.request.user, "teacher"):
            kwargs["teacher"] = self.request.user.teacher
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        course_id = self.kwargs.get("course_id")
        if course_id:
            initial["course"] = get_object_or_404(Course, pk=course_id)
        return initial

    def form_valid(self, form):
        if hasattr(self.request.user, "teacher"):
            form.instance.teacher = self.request.user.teacher
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("tasks_app:task_list")


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks_app/task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["today"] = date.today()
        task = self.object
        if hasattr(self.request.user, "student"):
            try:
                ctx["submission"] = Submission.objects.get(
                    task=task, student=self.request.user.student
                )
            except Submission.DoesNotExist:
                ctx["submission"] = None
        elif hasattr(self.request.user, "teacher"):
            ctx["submissions"] = task.submissions.all()
        return ctx


@method_decorator(student_required, name="dispatch")
class SubmissionCreateView(LoginRequiredMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "tasks_app/submission_form.html"

    def form_valid(self, form):
        task = get_object_or_404(Task, pk=self.kwargs["pk"])
        form.instance.task = task
        form.instance.student = self.request.user.student
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tasks_app:task_detail", kwargs={"pk": self.kwargs["pk"]})


@method_decorator(admin_or_teacher_required, name="dispatch")
class SubmissionGradeView(LoginRequiredMixin, UpdateView):
    model = Submission
    form_class = GradeSubmissionForm
    template_name = "tasks_app/submission_grade.html"
    context_object_name = "submission"

    def form_valid(self, form):
        if hasattr(self.request.user, "teacher"):
            form.instance.calificado_por = self.request.user.teacher
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tasks_app:task_detail", kwargs={"pk": self.object.task.pk})
