from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rut = models.CharField("RUT", max_length=12, unique=True)
    fecha_nacimiento = models.DateField("Fecha de nacimiento")
    telefono = models.CharField("Teléfono", max_length=15, blank=True)
    direccion = models.TextField("Dirección", blank=True)

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.rut}"

    @property
    def cursos_actuales(self):
        return self.courses.all()


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rut = models.CharField("RUT", max_length=12, unique=True)
    telefono = models.CharField("Teléfono", max_length=15, blank=True)
    fecha_contrato = models.DateField("Fecha de contrato")
    especialidad = models.CharField("Especialidad", max_length=100, blank=True)

    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"

    def __str__(self):
        return f"Prof. {self.user.get_full_name()}"


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rut = models.CharField("RUT", max_length=12, unique=True)
    telefono = models.CharField("Teléfono", max_length=15, blank=True)
    cargo = models.CharField("Cargo", max_length=100)

    class Meta:
        verbose_name = "Administrativo"
        verbose_name_plural = "Administrativos"

    def __str__(self):
        return f"{self.cargo}: {self.user.get_full_name()}"
