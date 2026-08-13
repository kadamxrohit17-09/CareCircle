# CareCircle Backend MVP

CareCircle is a family healthcare record and follow-up management platform built with Django.

## Tech Stack
- Django & Django REST Framework
- SimpleJWT (Authentication)
- SQLite (Local dev)
- Google Gemini (AI Analysis)

## Setup Instructions

1. **Clone & Virtual Environment**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment Variables**
Copy `.env.example` to `.env` and fill in your Gemini API Key.
```bash
cp .env.example .env
```

4. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create Superuser (Admin)**
```bash
python manage.py createsuperuser
```

6. **Run the Server**
```bash
python manage.py runserver
```

## API Documentation

- `POST /api/auth/register/` - Register user
- `POST /api/auth/login/` - Login and get JWT
- `GET /api/members/` - List family members
- `POST /api/reports/` - Upload medical report (multipart/form-data)
- `POST /api/reports/<id>/analyze/` - Trigger AI analysis on a report
- `GET /api/dashboard/` - Get user dashboard statistics
- `GET /api/members/<id>/timeline/` - View timeline of events

*Please note: CareCircle organizes medical information and is not a diagnostic tool.*
