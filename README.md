# 📚 Library Service

A Django REST API for managing books and borrowings in a library system.

## 🚀 Features

- **Books**: CRUD operations (admin-only for write access)
- **Borrowings**:
    - Users can borrow and return books
    - Book inventory updates automatically
    - Admins can filter borrowings by user or status
- **Authentication**: JWT-based login/registration system
- **Permissions**: Role-based access control for users and admins
- **Documentation**: Schema-based well-written documentation

## 🛠 Tech Stack

- Python
- Django
- Django REST Framework
- DRF-Spectacular
- Simple JWT
- SQLite (default)

## 🔧 Setup

1. **Clone the repository**

```bash
git clone https://github.com/mykola-tarasenko/library-service.git
cd library-service
```

2. **Create virtual environment and install dependencies**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

3. **Run migrations**

```bash
python manage.py migrate
```

4. **Create a superuser (admin panel access)**

```bash
python manage.py createsuperuser
```

5. **Run the development server**
```bash
python manage.py runserver
```
