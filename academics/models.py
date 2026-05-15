from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Course(models.Model):
    nombre = models.CharField("Nombre del curso", max_length=100)
    descripcion = models.TextField("Descripción", blank=True)
    año = models.IntegerField("Año académico")
    alumnos = models.ManyToManyField(
        "accounts.Student",
        related_name="courses",
        through="academics.Enrollment",
        blank=True,
    )

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["-año", "nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.año})"


class Subject(models.Model):
    nombre = models.CharField("Nombre", max_length=100)
    codigo = models.CharField("Código", max_length=10, unique=True)
    descripcion = models.TextField("Descripción", blank=True)
    profesores = models.ManyToManyField("accounts.Teacher", related_name="subjects", blank=True)
    cursos = models.ManyToManyField(Course, related_name="subjects", blank=True)

    class Meta:
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class Enrollment(models.Model):
    student = models.ForeignKey("accounts.Student", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    fecha_matricula = models.DateField("Fecha de matrícula", auto_now_add=True)

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        unique_together = ["student", "course"]

    def __str__(self):
        return f"{self.student} → {self.course}"


class Grade(models.Model):
    TIPO_NOTA_CHOICES = [
        ("PRUEBA", "Prueba"),
        ("TAREA", "Tarea"),
        ("EXAMEN", "Examen"),
        ("TRABAJO", "Trabajo"),
        ("CONTROL", "Control"),
        ("OTRO", "Otro"),
    ]

    student = models.ForeignKey("accounts.Student", on_delete=models.CASCADE, related_name="grades")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="grades")
    teacher = models.ForeignKey("accounts.Teacher", on_delete=models.SET_NULL, null=True, blank=True, related_name="grades_given")
    valor = models.DecimalField("Nota", max_digits=4, decimal_places=1, validators=[MinValueValidator(1.0), MaxValueValidator(7.0)])
    tipo_nota = models.CharField("Tipo", max_length=20, choices=TIPO_NOTA_CHOICES, default="PRUEBA")
    fecha = models.DateField("Fecha")
    observacion = models.TextField("Observación", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"
        ordering = ["-fecha", "-created_at"]

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.valor}"


class Attendance(models.Model):
    ESTADO_CHOICES = [
        ("PRESENTE", "Presente"),
        ("AUSENTE", "Ausente"),
        ("ATRASO", "Atraso"),
        ("JUSTIFICADO", "Justificado"),
    ]

    student = models.ForeignKey("accounts.Student", on_delete=models.CASCADE, related_name="attendances")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="attendances")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="attendances", null=True, blank=True)
    fecha = models.DateField("Fecha")
    estado = models.CharField("Estado", max_length=20, choices=ESTADO_CHOICES, default="PRESENTE")
    observacion = models.TextField("Observación", blank=True)
    registered_by = models.ForeignKey("accounts.Teacher", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        ordering = ["-fecha"]
        unique_together = ["student", "course", "fecha"]

    def __str__(self):
        return f"{self.student} - {self.fecha}: {self.get_estado_display()}"
