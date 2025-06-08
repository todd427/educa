# Educa

**Educa** is an e-learning platform built with Django. It allows instructors to create subjects, courses, modules, and learning content. This project is based on *Chapter 12* of the **Django 5 By Example** book and includes preloaded data via migrations.

---

## 🚀 Features

- Subject-based course organization (e.g., Mathematics, Music, etc.)
- Auto-generated 101-level courses for each subject
- Preloaded "Welcome" modules in each course
- Django admin for managing courses and users
- Internationalization-ready (i18n)
- GitHub integration with secure access token auth

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/todd427/educa.git
cd educa
```

### 2. Create and activate a virtual environment

```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run database migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Load initial data (optional if not using migrations)

```bash
python manage.py loaddata courses/fixtures/subjects.json
```

---

## 🧱 Development Tools

- Django 5.0.x
- Python 3.12+
- Git + GitHub
- SSH or Personal Access Token for GitHub auth

---

## 🧠 Project Notes

This project includes custom Django **data migrations** to preload:

- Subjects: Mathematics, Music, Physics, Programming
- Courses: Automatically generated `Subject 101` for each subject
- Modules: Each course includes a "Welcome" module with an introductory description

Migrations are saved under:  
`courses/migrations/0004_educa_initial_content.py`

---

## ✨ Author

**Todd McCaffrey**  
[github.com/todd427](https://github.com/todd427)  
[www.toddmccaffrey.org](https://www.toddmccaffrey.org)

---

## 📜 License

MIT License (or replace with your actual license)
