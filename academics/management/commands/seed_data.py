from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Student, Teacher, AdminProfile
from academics.models import Course, Subject, Enrollment, Grade, Attendance
from tasks_app.models import Task, Submission
import random


class Command(BaseCommand):
    help = "Crea datos de prueba para la aplicación"

    def handle(self, *args, **kwargs):
        self.stdout.write("Creando datos de prueba...")

        # ── Superuser / Admin ──
        if not User.objects.filter(username="admin").exists():
            admin_user = User.objects.create_superuser("admin", "admin@colegio.cl", "password123")
            admin_user.first_name = "Carlos"
            admin_user.last_name = "Muñoz"
            admin_user.save()
            AdminProfile.objects.create(
                user=admin_user, rut="5.555.555-5", telefono="+56 9 5555 5555", cargo="Director Académico"
            )
            self.stdout.write("  ✓ Admin creado")

        # ── Teachers ──
        teachers_data = [
            {"username": "profesor1", "first": "María", "last": "González", "rut": "12.345.678-9", "especialidad": "Matemáticas"},
            {"username": "profesor2", "first": "Pedro", "last": "López", "rut": "23.456.789-0", "especialidad": "Lenguaje"},
        ]
        teacher_objs = []
        for td in teachers_data:
            user, created = User.objects.get_or_create(
                username=td["username"],
                defaults={
                    "first_name": td["first"],
                    "last_name": td["last"],
                    "email": f'{td["username"]}@colegio.cl',
                },
            )
            if created:
                user.set_password("password123")
                user.save()
            teacher, _ = Teacher.objects.get_or_create(
                user=user, defaults={"rut": td["rut"], "telefono": "+56 9 1111 1111", "fecha_contrato": date(2023, 3, 1), "especialidad": td["especialidad"]}
            )
            teacher_objs.append(teacher)
            self.stdout.write(f"  ✓ Profesor {td['username']} creado")

        # ── Courses ──
        courses_data = [
            {"nombre": "1° Medio A", "año": 2026},
            {"nombre": "2° Medio A", "año": 2026},
            {"nombre": "3° Medio A", "año": 2026},
        ]
        course_objs = []
        for cd in courses_data:
            course, _ = Course.objects.get_or_create(nombre=cd["nombre"], año=cd["año"])
            course_objs.append(course)
            self.stdout.write(f"  ✓ Curso {cd['nombre']} creado")

        # ── Subjects ──
        subjects_data = [
            {"nombre": "Matemáticas", "codigo": "MAT01"},
            {"nombre": "Lenguaje", "codigo": "LEN01"},
            {"nombre": "Ciencias", "codigo": "CIE01"},
            {"nombre": "Historia", "codigo": "HIS01"},
            {"nombre": "Inglés", "codigo": "ING01"},
        ]
        subject_objs = []
        for sd in subjects_data:
            subj, _ = Subject.objects.get_or_create(codigo=sd["codigo"], defaults={"nombre": sd["nombre"]})
            subject_objs.append(subj)
            self.stdout.write(f"  ✓ Asignatura {sd['nombre']} creada")

        # ── Subject ↔ Teacher assignments ──
        teacher_objs[0].subjects.add(subject_objs[0], subject_objs[2], subject_objs[4])  # María: MAT, CIE, ING
        teacher_objs[1].subjects.add(subject_objs[1], subject_objs[3])  # Pedro: LEN, HIS

        # ── Subject ↔ Course assignments ──
        for course in course_objs:
            for subj in subject_objs:
                subj.cursos.add(course)

        # ── Students ──
        students_data = [
            {"username": "alumno1", "first": "Ana", "last": "Soto", "rut": "13.456.789-0", "course_idx": 0},
            {"username": "alumno2", "first": "Benjamín", "last": "Rojas", "rut": "14.567.890-1", "course_idx": 0},
            {"username": "alumno3", "first": "Catalina", "last": "Díaz", "rut": "15.678.901-2", "course_idx": 1},
            {"username": "alumno4", "first": "Diego", "last": "Torres", "rut": "16.789.012-3", "course_idx": 1},
            {"username": "alumno5", "first": "Emma", "last": "Valenzuela", "rut": "17.890.123-4", "course_idx": 2},
            {"username": "alumno6", "first": "Felipe", "last": "Martínez", "rut": "18.901.234-5", "course_idx": 2},
        ]
        student_objs = []
        for sd in students_data:
            user, created = User.objects.get_or_create(
                username=sd["username"],
                defaults={
                    "first_name": sd["first"],
                    "last_name": sd["last"],
                    "email": f'{sd["username"]}@colegio.cl',
                },
            )
            if created:
                user.set_password("password123")
                user.save()
            student, _ = Student.objects.get_or_create(
                user=user,
                defaults={
                    "rut": sd["rut"],
                    "fecha_nacimiento": date(2010, random.randint(1, 12), random.randint(1, 28)),
                    "telefono": "+56 9 2222 2222",
                    "direccion": f"Dirección de {sd['first']} {sd['last']}",
                },
            )
            student_objs.append(student)
            self.stdout.write(f"  ✓ Alumno {sd['username']} creado")

        # ── Enrollments ──
        for sd, student in zip(students_data, student_objs):
            course = course_objs[sd["course_idx"]]
            Enrollment.objects.get_or_create(student=student, course=course)

        # ── Grades ──
        tipos = ["PRUEBA", "TAREA", "EXAMEN", "CONTROL"]
        grade_count = 0
        for student in student_objs:
            course = student.courses.first()
            if not course:
                continue
            course_subjects = course.subjects.all()
            for subj in course_subjects:
                for _ in range(random.randint(1, 3)):
                    teacher = random.choice(subj.profesores.all() or teacher_objs)
                    Grade.objects.get_or_create(
                        student=student,
                        subject=subj,
                        tipo_nota=random.choice(tipos),
                        fecha=date(2026, random.randint(3, 5), random.randint(1, 28)),
                        defaults={
                            "teacher": teacher,
                            "valor": round(random.uniform(2.0, 7.0), 1),
                            "observacion": random.choice(["Buen trabajo", "Debe mejorar", "", "Excelente", "Regular"]),
                        },
                    )
                    grade_count += 1
        self.stdout.write(f"  ✓ {grade_count} notas creadas")

        # ── Tasks ──
        tasks_data = [
            {"titulo": "Ecuaciones de primer grado", "desc": "Resolver 20 ejercicios del libro páginas 45-50", "course_idx": 0, "subj_idx": 0, "teacher_idx": 0},
            {"titulo": "Ensayo literario", "desc": "Escribir un ensayo sobre 'El Quijote' (mínimo 2 páginas)", "course_idx": 1, "subj_idx": 1, "teacher_idx": 1},
            {"titulo": "Informe de laboratorio", "desc": "Realizar experimento de ósmosis y entregar informe", "course_idx": 2, "subj_idx": 2, "teacher_idx": 0},
        ]
        task_objs = []
        for td in tasks_data:
            task, _ = Task.objects.get_or_create(
                titulo=td["titulo"],
                subject=subject_objs[td["subj_idx"]],
                course=course_objs[td["course_idx"]],
                teacher=teacher_objs[td["teacher_idx"]],
                defaults={
                    "descripcion": td["desc"],
                    "fecha_entrega": date(2026, 6, random.randint(10, 25)),
                },
            )
            task_objs.append(task)
        self.stdout.write("  ✓ 3 tareas creadas")

        # ── Submissions ──
        for i, task in enumerate(task_objs):
            student = student_objs[i * 2]
            sub, _ = Submission.objects.get_or_create(
                task=task,
                student=student,
                defaults={
                    "comentario": "Aquí está mi entrega, profesor.",
                    "nota": round(random.uniform(3.0, 7.0), 1),
                    "feedback": random.choice(["Bien hecho", "Puedes mejorar", "Excelente trabajo", "Revisa la ortografía"]),
                    "calificado_por": task.teacher,
                },
            )

        # ── Attendance ──
        att_count = 0
        for student in student_objs:
            course = student.courses.first()
            if not course:
                continue
            for day_offset in range(5):
                d = date(2026, 4, 1) + timedelta(days=day_offset * 7)
                estado = random.choice(["PRESENTE", "PRESENTE", "PRESENTE", "AUSENTE", "ATRASO"])
                Attendance.objects.get_or_create(
                    student=student,
                    course=course,
                    fecha=d,
                    defaults={
                        "estado": estado,
                        "subject": random.choice(course.subjects.all() or subject_objs),
                        "registered_by": random.choice(teacher_objs),
                    },
                )
                att_count += 1
        self.stdout.write(f"  ✓ {att_count} asistencias registradas")

        self.stdout.write(self.style.SUCCESS("¡Datos de prueba creados exitosamente!"))
        self.stdout.write("")
        self.stdout.write("Usuarios de prueba:")
        self.stdout.write("  Admin:      admin / password123")
        self.stdout.write("  Profesor 1: profesor1 / password123")
        self.stdout.write("  Profesor 2: profesor2 / password123")
        self.stdout.write("  Alumno 1:   alumno1 / password123")
        self.stdout.write("  ... hasta alumno6 / password123")
