# PhiBook - Django REST API Project

A Django REST API project with authentication and user management.

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv env
   ```

3. Activate the virtual environment:
   - Windows: `env\Scripts\activate`
   - Linux/Mac: `source env/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

- `apps/authentication/` - Authentication API endpoints
- `apps/users/` - User management models and views
- `PhiBook/` - Main Django project settings

## API Endpoints

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/verify/<pk>/` - Account verification

## Dependencies

- Django 5.2.4
- Django REST Framework 3.14.0
- Django CORS Headers 4.3.1
- Python Decouple 3.8 