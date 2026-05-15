from django.urls import path
from . import views

app_name = "academics"

urlpatterns = [
    path("courses/", views.CourseListView.as_view(), name="course_list"),
    path("courses/create/", views.CourseCreateView.as_view(), name="course_create"),
    path("courses/<int:pk>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("courses/<int:pk>/edit/", views.CourseUpdateView.as_view(), name="course_edit"),
    path("courses/<int:pk>/delete/", views.CourseDeleteView.as_view(), name="course_delete"),
    path("subjects/", views.SubjectListView.as_view(), name="subject_list"),
    path("subjects/create/", views.SubjectCreateView.as_view(), name="subject_create"),
    path("grades/", views.GradeListView.as_view(), name="grade_list"),
    path("grades/create/", views.GradeCreateView.as_view(), name="grade_create"),
    path("grades/create/<int:course_id>/", views.GradeCreateView.as_view(), name="grade_create_for_course"),
    path("grades/<int:pk>/edit/", views.GradeUpdateView.as_view(), name="grade_edit"),
    path("attendance/", views.AttendanceListView.as_view(), name="attendance_list"),
    path("attendance/create/", views.AttendanceCreateView.as_view(), name="attendance_create"),
]
