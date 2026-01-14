# Local Development Guide

This guide helps you run the Django project locally on your development machine.

## Prerequisites

- Python 3.8+
- MySQL Server installed locally
- pip (Python package manager)

## Setup

### 1. Install MySQL (if not already installed)

**Windows:**
- Download from [MySQL Downloads](https://dev.mysql.com/downloads/installer/)
- Install and set root password

**macOS:**
```bash
brew install mysql
brew services start mysql
```

**Linux:**
```bash
sudo apt install mysql-server
sudo systemctl start mysql
```

### 2. Create Database

```bash
# Login to MySQL
mysql -uroot -p

# Create database
CREATE DATABASE allsy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Exit MySQL
exit
```

### 3. Set Up Python Environment

```bash
# Navigate to project directory
cd C:\Users\paguna\Desktop\magazia_back

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables

The `.env` file is already configured for local development with:
```env
DEBUG=True  # Enables development mode
DB_USER=root
DB_PASSWORD=Chuchu1!
DB_HOST=localhost
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

The server will start at: **http://127.0.0.1:8000**

**Important:** Access via HTTP (not HTTPS) when DEBUG=True

## Common Commands

### Run Server
```bash
python manage.py runserver
# Or on specific port
python manage.py runserver 8080
```

### Create Migrations
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### Collect Static Files
```bash
python manage.py collectstatic
```

### Django Shell
```bash
python manage.py shell
```

### Run Tests
```bash
python manage.py test
```

## Project Structure

```
magazia_back/
├── contacts/          # Contacts app
├── products/          # Products app
├── vueshop_backend/   # Main project settings
├── media/             # User uploaded files
├── staticfiles/       # Collected static files
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

## API Endpoints

Access the API at:
- Admin: http://127.0.0.1:8000/admin/
- API Root: http://127.0.0.1:8000/api/

## Development vs Production

### Local Development (.env)
```env
DEBUG=True              # Shows detailed errors
DB_USER=root           # Using MySQL root user
DB_HOST=localhost      # Local database
```

### Production (.env.production)
```env
DEBUG=False            # Hides error details
DB_USER=allsy_user     # Dedicated database user
DB_HOST=localhost      # On EC2 server
```

## Troubleshooting

### "You're accessing the development server over HTTPS"

This happens when:
- DEBUG=False and SECURE_SSL_REDIRECT=True
- You're trying to access via https://

**Solution:** Set `DEBUG=True` in your `.env` file for local development

### Database Connection Errors

```bash
# Verify MySQL is running
# Windows: Check Services app
# macOS: brew services list
# Linux: sudo systemctl status mysql

# Test MySQL connection
mysql -uroot -pChuchu1! -e "USE allsy; SHOW TABLES;"
```

### Port Already in Use

```bash
# Stop the process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

### Missing Dependencies

```bash
pip install -r requirements.txt
```

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
```

## CORS Settings

The project is configured to allow requests from:
- http://localhost:5173 (Vite dev server)
- http://localhost:5174
- https://allsy.ge
- https://www.allsy.ge

To add more origins, edit `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    # Add your frontend URL here
]
```

## Hot Reload

Django automatically reloads when you save Python files. No need to restart the server.

## Database GUI Tools

Recommended tools to manage your MySQL database:
- **MySQL Workbench** (Official, free)
- **DBeaver** (Free, multi-platform)
- **HeidiSQL** (Windows, free)
- **TablePlus** (macOS, paid with free tier)

## VS Code Configuration

Recommended extensions:
- Python
- Django
- MySQL

Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "[python]": {
        "editor.formatOnSave": true
    }
}
```

## Git Workflow

Before committing, ensure:
```bash
# Don't commit sensitive data
git status

# .env file should be in .gitignore (already configured)
# Check .gitignore includes:
# .env
# venv/
# __pycache__/
# db.sqlite3
```

## Switch Between Development and Production

### For Local Development:
```bash
# Use current .env with DEBUG=True
python manage.py runserver
```

### For Production Testing Locally:
```bash
# Copy production settings
cp .env.production .env

# Run with Gunicorn
gunicorn --config gunicorn_config.py vueshop_backend.wsgi:application
```

### For EC2 Production:
```bash
# Use .env.production on server with DEBUG=False
```

## Next Steps

1. Start development server: `python manage.py runserver`
2. Access admin panel: http://127.0.0.1:8000/admin/
3. Test API endpoints
4. Build your frontend to connect to http://127.0.0.1:8000

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
