def user_role(request):
    if not request.user.is_authenticated:
        return {"role": None}
    if hasattr(request.user, "student"):
        return {"role": "student"}
    if hasattr(request.user, "teacher"):
        return {"role": "teacher"}
    if hasattr(request.user, "adminprofile") or request.user.is_superuser:
        return {"role": "admin"}
    return {"role": None}
