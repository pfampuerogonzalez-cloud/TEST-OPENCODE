from django.urls import path
from . import views

app_name = "tasks_app"

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task_list"),
    path("create/", views.TaskCreateView.as_view(), name="task_create"),
    path("create/<int:course_id>/", views.TaskCreateView.as_view(), name="task_create_for_course"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("<int:pk>/submit/", views.SubmissionCreateView.as_view(), name="submission_create"),
    path("submissions/<int:pk>/grade/", views.SubmissionGradeView.as_view(), name="submission_grade"),
]
