from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Task(models.Model):
    titulo = models.CharField("Título", max_length=200)
    descripcion = models.TextField("Descripción")
    subject = models.ForeignKey("academics.Subject", on_delete=models.CASCADE, related_name="tasks")
    teacher = models.ForeignKey("accounts.Teacher", on_delete=models.CASCADE, related_name="tasks")
    course = models.ForeignKey("academics.Course", on_delete=models.CASCADE, related_name="tasks")
    fecha_creacion = models.DateTimeField("Fecha de creación", auto_now_add=True)
    fecha_entrega = models.DateField("Fecha de entrega")
    archivo = models.FileField("Archivo adjunto", upload_to="tasks/", blank=True, null=True)

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ["-fecha_entrega"]

    def __str__(self):
        return self.titulo


class Submission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey("accounts.Student", on_delete=models.CASCADE, related_name="submissions")
    fecha_entrega = models.DateTimeField("Fecha de entrega", auto_now_add=True)
    archivo = models.FileField("Archivo", upload_to="submissions/", blank=True, null=True)
    comentario = models.TextField("Comentario", blank=True)
    nota = models.DecimalField(
        "Nota",
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(7.0)],
        null=True,
        blank=True,
    )
    feedback = models.TextField("Retroalimentación", blank=True)
    calificado_por = models.ForeignKey(
        "accounts.Teacher", on_delete=models.SET_NULL, null=True, blank=True, related_name="graded_submissions"
    )

    class Meta:
        verbose_name = "Entrega"
        verbose_name_plural = "Entregas"
        unique_together = ["task", "student"]
        ordering = ["-fecha_entrega"]

    def __str__(self):
        return f"{self.student} → {self.task.titulo}"
