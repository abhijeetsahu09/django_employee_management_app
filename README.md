# Django CRM Project

This is a Customer Relationship Management (CRM) system built using Django, designed to manage customer interactions, sales pipelines, and more. The application utilizes a MySQL database for data storage and management.

## Features

- **Customer Management:** Store and manage customer information.
- **Task Management:** Assign and track tasks related to customers.
- **Reporting:** Generate reports for customer interactions, and more.

## Requirements

- Python 3.x
- Django 3.x
- MySQL

## Installation

1. **Clone the repository:**

    ```bash
    git@github.com:abhijeetsahu09/Django-CRM.git
    cd Django-CRM
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On macOS and Linux
    venv\Scripts\activate      # On Windows
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the MySQL database:**

    - Create a MySQL database.
    - Update the database configurations in `settings.py`:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    ```

5. **Run migrations and start the development server:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```

6. **Access the application:**

    Open your web browser and go to `http://localhost:8000`.

## Usage

- **Admin Panel:** Access the Django admin panel at `/admin` to manage customers, tasks, and more.
- **API Endpoints:** Explore and utilize the available API endpoints for custom integrations or automation.

## Contributing

Contributions are welcome! Feel free to submit issues, feature requests, or pull requests.

## Acknowledgments

- This project was inspired by the need for a comprehensive CRM solution using Django and MySQL.
- Special thanks to the Django and MySQL communities for their valuable resources and documentation.
