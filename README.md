# Doctor Appointment Booking System

![Stars](https://img.shields.io/github/stars/JavadMoradkhah/doctor-appointment-booking?style=social)
![Views](https://img.shields.io/github/watchers/JavadMoradkhah/doctor-appointment-booking?style=social)
![Python Version](https://img.shields.io/badge/python-3.11-blue)
![Django Version](https://img.shields.io/badge/django-4.2-green)
![Project Version](https://img.shields.io/badge/version-1.0.0-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)
![Last Commit](https://img.shields.io/github/last-commit/JavadMoradkhah/doctor-appointment-booking)
![Open Issues](https://img.shields.io/github/issues/JavadMoradkhah/doctor-appointment-booking)
![Build Status](https://img.shields.io/github/workflow/status/JavadMoradkhah/doctor-appointment-booking/CI)
![Contributors](https://img.shields.io/github/contributors/JavadMoradkhah/doctor-appointment-booking)
![Closed Issues](https://img.shields.io/github/issues-closed/JavadMoradkhah/doctor-appointment-booking)
![Dependencies](https://img.shields.io/david/JavadMoradkhah/doctor-appointment-booking)


The **Doctor Appointment Booking System** is a web-based appointment scheduling system similar to **Paziresh24**, designed specifically for a single clinic. This application allows patients to book appointments, doctors to manage their schedules, and clinic administrators to oversee operations. It also implements secure OTP-based authentication.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Environment Variables](#environment-variables)
- [Docker Setup](#docker-setup)
- [Database Migrations](#database-migrations)
- [Loading Initial Data (Fixtures)](#loading-initial-data-fixtures)
- [Running Tests](#running-tests)
- [Celery Tasks](#celery-tasks)
- [Useful Commands](#useful-commands)
- [Contributing](#contributing)

## Features

- **OTP Authentication**: Login and signup using One Time Password (OTP) for secure access.
- **Appointment Scheduling**: Patients can book appointments with available doctors.
- **Admin Dashboard**: Manage users, doctors, appointments, and system configurations.
- **Doctor’s Portal**: Doctors can manage their appointments and availability.
- **Background Tasks**: Celery and Redis handle tasks like sending OTPs and email notifications.
- **PostgreSQL Database**: For reliable data storage of appointments, users, and schedules.

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Authentication**: JWT + OTP (One Time Password)
- **Task Queue**: Celery with Redis as the broker
- **Database**: PostgreSQL
- **Containerization**: Docker and Docker Compose

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/JavadMoradkhah/doctor-appointment-booking.git
   cd server
   ```

2. Install dependencies using `pipenv`:
   ```bash
   pipenv install --system
   pipenv shell
   ```

3. Set up environment variables:
   Create a `.env.dev` file in the `server/` directory using the provided `.env.example` as a template.

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Load initial data (optional):
   ```bash
   python manage.py loaddata provinces.json
   python manage.py loaddata cities.json
   python manage.py loaddata insurances.json
   python manage.py loaddata facilities.json
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Running the Application

Once all the steps in the installation process are completed, you can run the application using either local development tools or Docker.

### Local Development

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Access the application at `http://localhost:8000`.

### Docker Setup

To run the application with Docker:

1. Build and start the services:
   ```bash
   docker compose up --build
   ```

2. Access the application at `http://localhost:8000`.

### Docker Services

- **Server**: Django application served via Gunicorn on port `8000`.
- **Database**: PostgreSQL 16.3 with persistent data stored in a Docker volume.
- **Redis**: Redis 7.2.4 for caching and task queue management.
- **Celery**: Celery worker for background tasks.
- **Adminer**: Web-based database management on port `8080`.

## Environment Variables

You should create a `.env.dev` file in the `server/` directory with the following variables:

```env
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@database:5432/db_name
REDIS_URL=redis://redis:6379
```

These variables control the environment settings, database, and Redis connections.

## Database Migrations

To create and apply database migrations, run:

```bash
docker compose exec server python manage.py makemigrations
docker compose exec server python manage.py migrate
```

## Loading Initial Data (Fixtures)

If you need to populate the database with initial data like provinces, cities, or insurances, use:

```bash
docker compose exec -it server python manage.py loaddata provinces.json
docker compose exec -it server python manage.py loaddata cities.json
docker compose exec -it server python manage.py loaddata insurances.json
docker compose exec -it server python manage.py loaddata facilities.json
```

## Running Tests

To run the test suite, execute:

```bash
docker compose exec server python manage.py test
```

This will run all unit tests defined in the project to ensure the integrity of the application.

## Celery Tasks

The project uses Celery for background tasks, such as sending OTPs and processing emails. To manually start Celery in a development environment, run:

```bash
celery -A config worker --loglevel=info
```

In Docker, Celery will start automatically.

## Useful Commands

- **Create a superuser**:
   ```bash
   docker compose exec server python manage.py createsuperuser
   ```

- **Access the Admin Panel**:
   Visit `http://localhost:8000/admin/` and log in with your superuser credentials.

## Contributing

We welcome contributions! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

Please ensure any new code has accompanying tests and follows the coding standards.

---

