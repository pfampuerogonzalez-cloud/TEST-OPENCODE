from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Student, Teacher, AdminProfile


class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False


class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False


class AdminProfileInline(admin.StackedInline):
    model = AdminProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [StudentInline, TeacherInline, AdminProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(AdminProfile)
