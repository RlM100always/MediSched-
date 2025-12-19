# MediSched

MediSched is a Django-based medical appointment scheduling system with admin, doctor, and patient interfaces.

## Features

- User authentication (Admin, Doctor, Patient)
- Appointment booking and management
- Analytics dashboard
- Doctor and department management

## Requirements

- Python 3.8+
- pip (Python package manager)
- (Optional) Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repo-url>
cd MediSched-Project/medisched
```

### 2. Create and Activate a Virtual Environment

On Windows:
```bash
python -m venv env
env\Scripts\activate
```
On macOS/Linux:
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Create a Superuser

```bash
python manage.py createsuperuser
```
Follow the prompts to set up an admin account.

### 6. Run the Development Server

```bash
python manage.py runserver
```

### 7. Access the Application

- Open your browser and go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Notes

- Default database is SQLite (db.sqlite3).
- Static and media files are managed by Django settings.
- For any issues, check the terminal output for error messages.

## Project Structure

```
medisched/
├── adminapp/
├── appointment/
├── communication/
├── core/
├── doctor/
├── home/
├── users/
├── media/
├── manage.py
├── requirements.txt
└── ...
```


