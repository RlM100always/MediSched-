# Copilot Instructions for MediSched

**MediSched** is a Django 5.2 telemedicine appointment scheduling platform with doctor-patient interactions, video consultations, and payment processing.

## Architecture Overview

### Core Models & Data Flow

```
CustomUser (users.models)
├── Patient (role='patient')
└── Doctor (role='doctor')
    ├── Specializations: Department, Symptom (M2M)
    ├── Location: Division → District → Upazila (hierarchical)
    └── DoctorAppointmentFee: consultation fees (General/Special)

Appointment (appointment.models)
├── Links: Patient → Doctor
├── Status: pending → confirmed → completed/cancelled
├── Payment: consultation_fee + vat_amount + platform_fee (29.00)
├── Types: instant (video) or scheduled
└── Tracks: actual_start_time, actual_end_time, doctor_notes, follow_up

Communication (communication.models)
├── Conversation (1:1 per Appointment)
├── Message: text/image/file/prescription/test_report/audio
└── Prescription: diagnosis, advice, follow_up_date
```

### App Structure

- **users**: CustomUser model with role-based access (patient/doctor)
- **doctor**: Doctor profiles, specializations, fees, experience
- **adminapp**: Reference data (Departments, Symptoms, Divisions, Districts, Upazilas)
- **appointment**: Booking, status tracking, payments, follow-ups
- **communication**: Chat, video calls (Agora SDK), prescriptions
- **home**: Public-facing pages (doctor search, department/symptom browsing)
- **core**: Shared utilities

### External Integrations

- **Agora SDK**: Video/audio consultation via `communication/agora_utils.py`
  - Requires `AGORA_APP_ID` and `AGORA_APP_CERTIFICATE` in settings
  - Generates RTC tokens with 1-hour default expiry
- **Payment Methods**: bKash, Nagad, Card, Mobile Banking
- **Deployment**: Render.com (WhiteNoise middleware for static files)

## Key Development Patterns

### Authentication & Authorization

- Use `@role_required('patient')` or `@role_required('doctor')` decorator from `users.decorators`
- Always check `request.user.is_authenticated` before accessing user data
- CustomUser has `is_patient()` and `is_doctor()` helper methods

### Database Queries

- **Prevent IntegrityError**: Doctor ForeignKeys use `on_delete=models.SET_NULL, null=True, blank=True`
- **Prevent Duplicates**: Use `unique_together` in Meta class
  - Example: `('doctor', 'department')` for DoctorSpecializationDepartment
- **Hierarchical Location**: Always query `Upazila → District → Division` chain
- **M2M Through Models**: Doctor specializations use intermediate tables for flexible data

### Media Handling

- Images: `upload_to='doctor_profiles/'`, `upload_to='department/'`, `upload_to='symptoms/'`
- Files: `upload_to='prescriptions/'`, `upload_to='test_reports/'`, `upload_to='communication/files/'`
- Images use Pillow (PIL) for processing
- WhiteNoise serves static files in production

### Transaction Management

- Appointment creates auto-generated `transaction_id` (format: `APPT-{12-char hex}`) on first paid status
- All payment fields are Decimal: `max_digits=10, decimal_places=2`
- Payment status transitions: pending → paid/failed → refunded

## Critical Workflows

### Running the Project

```bash
# Navigate to project root
cd medisched/

# Run migrations (creates db.sqlite3)
python manage.py migrate

# Create superuser (for /admin)
python manage.py createsuperuser

# Development server (http://localhost:8000)
python manage.py runserver
```

### Common Django Commands

```bash
# Make migrations for model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create app-specific migrations
python manage.py makemigrations doctor

# Check for migration conflicts
python manage.py showmigrations
```

### Database Structure

- **SQLite3** (development/default): `db.sqlite3`
- Migrations tracked in `app/migrations/` folders
- Always run migrations before testing model changes

## Code Organization Conventions

### Views Pattern

- Function-based views in each app's `views.py`
- Protected endpoints check `request.user.role` or use `@role_required` decorator
- Return JSON for AJAX; templates for page renders

### Model Constraints

- Use `class Meta` for `unique_together`, ordering, and verbose names
- Always include `__str__()` methods for readable admin representation
- Use JSONField for flexible data (e.g., `working_hours: {"Mon": "9-5"}`)

### Forms Pattern

- Located in `app/forms.py`
- Extend Django's `ModelForm` or authentication forms
- Example: `CustomUserSignupForm` (users.forms)

### URL Routing

- Apps define `urls.py` with their routes
- Namespace apps: `path('appointment/', include('appointment.urls', namespace='appointment'))`
- Root urls.py (`medisched/urls.py`) includes all app URLs

## Important Details

### Rating & Review System

- `Doctor.rating`: DecimalField (0.0-5.0), `max_digits=3, decimal_places=2`
- `Doctor.total_reviews`: counter for normalization
- Updated after appointment completion

### Appointment Fee Categories

- Only two: `'General'` (General Consultation) and `'Special'` (Special Consultation)
- One fee per doctor per category (enforced via unique_together)
- Use `DoctorAppointmentFee` model to fetch doctor's consultation cost

### Video Call Setup

- Call Agora token generation before consultation starts
- Token includes `channel_name` (unique per conversation), `uid` (user ID)
- Conversation is 1:1 linked to Appointment (OneOneField)

### Filtering & Sorting

- Doctor list default sort: by 'verified' status (not rating)
- Filter by department, symptom, location (Division/District/Upazila)
- Use Django ORM filtering with `filter()`, not raw SQL

## Testing & Validation

- Models include validators (e.g., `PositiveIntegerField` for age, experience)
- Transaction IDs are unique to prevent duplicate payments
- Follow-up scheduling: `follow_up_date` must be after current appointment
- File uploads validated by FileField (PDFs, images for test reports)

## Deployment Considerations

- **Static Files**: WhiteNoise serves in production (configured in middleware)
- **Media Files**: Served via `settings.MEDIA_URL` and `settings.MEDIA_ROOT`
- **Debug**: `DEBUG=True` for development, `False` for production
- **Secrets**: `SECRET_KEY`, Agora credentials in environment variables (not hardcoded)
