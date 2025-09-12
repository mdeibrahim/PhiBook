# PhiBook

## Overview
PhiBook is a Django-based project for user authentication, dashboard management, and more.

## Getting Started
1. Clone the repository.
2. Set up a Python virtual environment and install dependencies:
   ```cmd
   cd PhiBook
   env\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```cmd
   python manage.py migrate
   ```
4. Start the development server:
   ```cmd
   python manage.py runserver
   ```

## API Documentation
- The API is documented using drf-spectacular and can be viewed at `/api/v1/docs/` when the server is running.

## Postman Collection
A Postman collection is provided for easy API testing. Import the following file into Postman:

- [`PhiBook.postman_collection.json`](PhiBook.postman_collection.json)

## Folder Structure
- `apps/` - Django apps (authentication, dashboard, users)
- `PhiBook/` - Project settings and configuration
- `staticfiles/` - Static assets
- `requirements.txt` - Python dependencies
- `vercel.json` - Vercel deployment config

`Thank you for visit`


