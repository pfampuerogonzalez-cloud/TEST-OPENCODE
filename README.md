# Gestión Académica

Sistema de gestión escolar con roles de **Alumno**, **Profesor** y **Administrativo**.

## Stack

- Python 3.12+ / Django 6.0
- PostgreSQL
- Bootstrap 5 (UI)
- Django Templates (server-side rendering)

## Requisitos previos

- Python 3.12 o superior
- PostgreSQL 14+
- pip

## Setup rápido

### 1. Clonar e instalar dependencias

```bash
git clone <repo>
cd gestion_academica
python -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 2. Configurar PostgreSQL

```bash
# Entrar a psql y crear la base de datos
sudo -u postgres psql
CREATE DATABASE gestion_academica;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE gestion_academica TO postgres;
\q
```

> Si usas credenciales distintas, configúralas como variables de entorno:
> ```bash
> export DB_NAME=gestion_academica
> export DB_USER=postgres
> export DB_PASSWORD=postgres
> export DB_HOST=localhost
> export DB_PORT=5432
> ```

### 3. Migrar y poblar la base de datos

```bash
python manage.py migrate
python manage.py seed_data
```

### 4. Ejecutar

```bash
python manage.py runserver
```

Abrir http://127.0.0.1:8000

---

## Usuarios de prueba

| Usuario     | Contraseña  | Rol           |
|-------------|-------------|---------------|
| `admin`     | password123 | Administrativo |
| `profesor1` | password123 | Profesor       |
| `profesor2` | password123 | Profesor       |
| `alumno1`   | password123 | Alumno (1° Medio A) |
| `alumno2`   | password123 | Alumno (1° Medio A) |
| `alumno3`   | password123 | Alumno (2° Medio A) |
| `alumno4`   | password123 | Alumno (2° Medio A) |
| `alumno5`   | password123 | Alumno (3° Medio A) |
| `alumno6`   | password123 | Alumno (3° Medio A) |

---

## Funcionalidades por rol

### Alumno
- Dashboard con notas recientes y tareas pendientes
- Ver notas por asignatura
- Ver tareas del curso y entregarlas
- Ver asistencia

### Profesor
- Dashboard con asignaturas a cargo
- Subir/editar notas por curso y asignatura
- Crear tareas para sus cursos
- Revisar entregas y calificar
- Registrar asistencia

### Administrativo
- Dashboard con estadísticas (alumnos, profesores, cursos)
- CRUD completo de alumnos y profesores
- CRUD de cursos y asignaturas
- Acceso a notas, tareas y asistencia de toda la institución

---

## Estructura del proyecto

```
gestion_academica/
├── config/              # Configuración del proyecto
│   ├── settings.py
│   └── urls.py
├── accounts/            # Perfiles de usuario (Student, Teacher, Admin)
│   ├── models.py
│   ├── views.py
│   ├── decorators.py    # @student_required, @teacher_required, @admin_required
│   └── templates/accounts/
├── academics/           # Cursos, asignaturas, notas, asistencia
│   ├── models.py
│   ├── views.py
│   ├── management/commands/seed_data.py
│   └── templates/academics/
├── tasks_app/           # Tareas y entregas
│   ├── models.py
│   ├── views.py
│   └── templates/tasks_app/
├── templates/           # Templates base (base.html, dashboard.html, login)
└── media/               # Archivos subidos (tareas, entregas)
```
