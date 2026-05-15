from django.contrib import admin
from .models import Course, Subject, Enrollment, Grade, Attendance

admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Enrollment)
admin.site.register(Grade)
admin.site.register(Attendance)
