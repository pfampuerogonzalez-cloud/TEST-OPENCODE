from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        if hasattr(request.user, "student"):
            return view_func(request, *args, **kwargs)
        messages.error(request, "Acceso solo para alumnos.")
        return redirect("dashboard")
    return _wrapped_view


def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        if hasattr(request.user, "teacher"):
            return view_func(request, *args, **kwargs)
        messages.error(request, "Acceso solo para profesores.")
        return redirect("dashboard")
    return _wrapped_view


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        if hasattr(request.user, "adminprofile") or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Acceso solo para administrativos.")
        return redirect("dashboard")
    return _wrapped_view


def admin_or_teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        if hasattr(request.user, "teacher") or hasattr(request.user, "adminprofile") or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Acceso solo para profesores o administrativos.")
        return redirect("dashboard")
    return _wrapped_view
