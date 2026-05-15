from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .forms import LoginForm

app_name = "accounts"

urlpatterns = [
    path("login/", LoginView.as_view(template_name="registration/login.html", redirect_authenticated_user=True, authentication_form=LoginForm), name="login"),
    path("logout/", LogoutView.as_view(next_page="accounts:login"), name="logout"),
    path("students/", views.StudentListView.as_view(), name="student_list"),
    path("students/create/", views.StudentCreateView.as_view(), name="student_create"),
    path("students/<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    path("teachers/", views.TeacherListView.as_view(), name="teacher_list"),
    path("teachers/create/", views.TeacherCreateView.as_view(), name="teacher_create"),
    path("teachers/<int:pk>/", views.TeacherDetailView.as_view(), name="teacher_detail"),
]
