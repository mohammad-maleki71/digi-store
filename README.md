# 🚀 Digital Store Backend API

A scalable and production-ready backend API for a Digital Store built with **Django REST Framework**.

This project implements a secure authentication system using JWT, email verification, phone verification (OTP), Redis, Celery, PostgreSQL, and API documentation with Swagger.

---

# 📑 Table of Contents

* Features
* Tech Stack
* Project Architecture
* Screenshots
* Installation
* Environment Variables
* Database Setup
* Running Redis
* Running Celery
* Running the Project
* API Documentation
* Authentication Flow
* API Endpoints
* Project Structure
* Running Tests
* Logging
* Security
* Future Improvements
* License

---

# ✨ Features

* Custom User Model
* JWT Authentication
* User Registration
* Login
* Logout
* Refresh Token
* Email Verification
* Phone Verification (OTP)
* User Profile
* Profile Update
* Redis Cache
* Celery Background Tasks
* PostgreSQL
* Swagger Documentation
* Unit Testing
* Custom Exception Handler
* Logging
* Clean Service Layer Architecture

---

# 🛠 Tech Stack

Backend

* Python
* Django
* Django REST Framework

Database

* PostgreSQL

Authentication

* JWT (Simple JWT)

Cache

* Redis

Background Tasks

* Celery

Documentation

* drf-spectacular (Swagger)

Storage

* Arvan Cloud (S3 Compatible)

Deployment (Planned)

* Docker
* Gunicorn
* Nginx
* CI/CD

---

# 🏗 Project Architecture

```
Client
    │
    ▼
DRF Views
    │
    ▼
Serializers
    │
    ▼
Services
    │
    ▼
Models
    │
    ▼
PostgreSQL
```

Background Tasks

```
Request
   │
   ▼
Redis
   │
   ▼
Celery Worker
   │
   ▼
Email / SMS
```

---

# 📸 Screenshots

## Swagger

> Add screenshot here

```
screenshots/swagger.png
```

---

## Registration

> Add screenshot here

```
screenshots/register.png
```

---

## Login

> Add screenshot here

```
screenshots/login.png
```

---

## User Profile

> Add screenshot here

```
screenshots/profile.png
```

---

## Celery Worker

> Add screenshot here

```
screenshots/celery.png
```

---

## Redis

> Add screenshot here

```
screenshots/redis.png
```

---

## Tests

> Add screenshot here

```
screenshots/tests.png
```

---

# ⚙ Installation

Clone repository

```bash
git clone https://github.com/your-username/digital_store.git
```

Enter project

```bash
cd digital_store
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

Windows

```bash
venv\Scripts\activate
```

Linux

```bash
source venv/bin/activate
```

Install packages

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a .env file

```
SECRET_KEY=

DEBUG=True

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

REDIS_URL=
```

---

# 🗄 Database

Run migrations

```bash
python manage.py migrate
```

Create superuser

```bash
python manage.py createsuperuser
```

---

# 📦 Run Redis

```bash
redis-server
```

---

# ⚡ Run Celery

```bash
celery -A config worker -l info
```

---

# ▶ Run Server

```bash
python manage.py runserver
```

---

# 📚 API Documentation

Swagger

```
/api/schema/swagger-ui/
```

Redoc

```
/api/schema/redoc/
```

---

# 🔐 Authentication Flow

```
Register
     │
     ▼
Verification Email
     │
     ▼
Verification Phone
     │
     ▼
User Created
     │
     ▼
Login
     │
     ▼
JWT Access Token
     │
     ▼
Protected APIs
```

---

# 📌 API Endpoints

| Method | Endpoint        | Description      |
| ------ | --------------- | ---------------- |
| POST   | /register/      | Register User    |
| POST   | /login/         | Login            |
| POST   | /logout/        | Logout           |
| POST   | /token/refresh/ | Refresh Token    |
| GET    | /verify-email/  | Verify Email     |
| POST   | /verify-phone/  | Verify Phone     |
| GET    | /profile/       | Retrieve Profile |
| PATCH  | /profile/       | Update Profile   |

---

# 📁 Project Structure

```
digital_store/

├── accounts/
├── config/
├── core/
├── media/
├── static/
├── screenshots/
├── manage.py
├── requirements.txt
└── README.md
```

---

# 🧪 Running Tests

Run all tests

```bash
python manage.py test
```

Run app tests

```bash
python manage.py test accounts
```

---

# 📝 Logging

Logging is configured to record:

* Errors
* Exceptions
* API Failures

---

# 🔒 Security

* JWT Authentication
* Password Hashing
* Custom User Model
* Email Verification
* Phone Verification
* Redis Token Storage
* Token Blacklisting
* Input Validation

---

# 🚀 Future Improvements

* Docker
* Gunicorn
* Nginx
* CI/CD
* Rate Limiting
* Object-Level Permissions
* Social Authentication
* API Versioning
* Monitoring
* Prometheus
* Grafana

---

# 📄 License

MIT License

---

# 👨‍💻 Author

Mohammad Maleki

Backend Developer

Python • Django • Django REST Framework
