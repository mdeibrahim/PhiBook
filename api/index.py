import os
import sys
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_dir))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PhiBook.settings')

# Import Django and create WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# For Vercel
app = application
