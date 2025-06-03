# Bookshop

## Overview
Bookshop is an online platform designed to manage and sell books efficiently. This project provides functionality for book listings, user authentication, and order management.

## Features
- **User Authentication**: Users can sign up, log in, and manage their accounts.
- **Book Management**: Add, edit, and remove books from the store.
- **Order System**: Users can purchase books and track their orders.
- **Admin Panel**: Admin users can manage books, orders, and customers.

## Technologies Used
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **Version Control**: Git & GitHub

## Environment Configuration
This project uses a `.env` file to manage sensitive settings like the database configuration.

### 1. Create a `.env` file in the project root and add the following:
```ini
SECRET_KEY=your_secret_key
DEBUG=True

# Database Configuration
DB_NAME=bookshop
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
```

### 2. Ensure the `.env` file is loaded in `settings.py`:
```python
import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=True)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
```

## Installation
1. Clone the repository:
   ```bash
   git clone git@github.com:SHOXAKONG/Bookshop.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Bookshop
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a `.env` file and configure it as shown above.
6. Apply migrations:
   ```bash
   python manage.py migrate
   ```
7. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```
8. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage
- Visit `http://127.0.0.1:8000/` in your browser.
- Register an account or log in.
- Browse available books and add them to your cart.
- Place orders and manage them from your dashboard.
- Admin users can log in at `/admin/` to manage books and orders.

## Managing Books with Django Admin
Django provides a built-in admin panel to manage books efficiently. To use it:
1. Register the `Book` model in `admin.py`:
   ```python
   from django.contrib import admin
   from .models import Book

   @admin.register(Book)
   class BookAdmin(admin.ModelAdmin):
       list_display = ('title', 'author', 'price', 'available')
       search_fields = ('title', 'author')
       list_filter = ('available',)
   ```
2. Log in to the Django admin panel at `/admin/` using your superuser credentials.
3. Navigate to the **Books** section to add, edit, or remove books.

## Contribution
Contributions are welcome! Feel free to fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries or suggestions, feel free to reach out at [your email or GitHub profile].

