-- ------------------------------
-- Lookup Tables
-- ------------------------------

CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE genders (
    gender_id SERIAL PRIMARY KEY,
    gender_name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE appointment_status (
    status_id SERIAL PRIMARY KEY,
    status_name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE reminder_types (
    reminder_type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE reminder_status (
    reminder_status_id SERIAL PRIMARY KEY,
    status_name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE payment_methods (
    method_id SERIAL PRIMARY KEY,
    method_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE payment_status (
    status_id SERIAL PRIMARY KEY,
    status_name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE blood_group (
    blood_group_id SERIAL PRIMARY KEY,
    blood_group_name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE divisions (
    division_id SERIAL PRIMARY KEY,
    division_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE districts (
    district_id SERIAL PRIMARY KEY,
    district_name VARCHAR(100) NOT NULL,
    division_id INT NOT NULL REFERENCES divisions(division_id) ON DELETE CASCADE,
    UNIQUE(district_name, division_id)
);

CREATE TABLE upazilas (
    upazila_id SERIAL PRIMARY KEY,
    upazila_name VARCHAR(100) NOT NULL,
    district_id INT NOT NULL REFERENCES districts(district_id) ON DELETE CASCADE,
    UNIQUE(upazila_name, district_id)
);

CREATE TABLE symptoms (
    symptom_id SERIAL PRIMARY KEY,
    symptom_name VARCHAR(100) UNIQUE NOT NULL,
    symptom_image VARCHAR(255)
);

CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) UNIQUE NOT NULL,
    department_image VARCHAR(255)
);

-- ------------------------------
-- Core User Tables
-- ------------------------------

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role_id INT NOT NULL REFERENCES roles(role_id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE patients (
    patient_id INT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    date_of_birth DATE,
    gender_id INT REFERENCES genders(gender_id),
    division_id INT REFERENCES divisions(division_id),
    district_id INT REFERENCES districts(district_id),
    upazila_id INT REFERENCES upazilas(upazila_id),
    exact_location VARCHAR(255),
    blood_group_id INT REFERENCES blood_group(blood_group_id),
    medical_history TEXT
);

CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    about TEXT,
    bmdc_number VARCHAR(255),
    qualification VARCHAR(255),
    total_experience INT DEFAULT 0,
    working_hours JSONB,
    profile_image VARCHAR(255),
    is_verified BOOLEAN DEFAULT FALSE,
    division_id INT REFERENCES divisions(division_id),
    district_id INT REFERENCES districts(district_id),
    upazila_id INT REFERENCES upazilas(upazila_id)
);

CREATE TABLE doctor_experience (
    id SERIAL PRIMARY KEY,
    doctor_id INT NOT NULL REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    hospital_name VARCHAR(255),
    designation VARCHAR(255),
    department VARCHAR(255)
);

CREATE TABLE doctor_specialization_departments (
    doctor_id INT NOT NULL REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    department_id INT NOT NULL REFERENCES departments(department_id) ON DELETE CASCADE,
    PRIMARY KEY (doctor_id, department_id)
);

CREATE TABLE doctor_specialization_symptoms (
    doctor_id INT NOT NULL REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    symptom_id INT NOT NULL REFERENCES symptoms(symptom_id) ON DELETE CASCADE,
    PRIMARY KEY (doctor_id, symptom_id)
);

CREATE TABLE admins (
    admin_id INT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    role_description TEXT
);

-- ------------------------------
-- Appointment & Consultation
-- ------------------------------

CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patients(patient_id),
    doctor_id INT NOT NULL REFERENCES doctors(doctor_id),
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status_id INT REFERENCES appointment_status(status_id),
    reason TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(patient_id, appointment_date, appointment_time),
    UNIQUE(doctor_id, appointment_date, appointment_time)
);

CREATE TABLE reminders (
    reminder_id SERIAL PRIMARY KEY,
    appointment_id INT NOT NULL REFERENCES appointments(appointment_id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES users(user_id),
    reminder_type_id INT NOT NULL REFERENCES reminder_types(reminder_type_id),
    message TEXT NOT NULL,
    sent_at TIMESTAMP,
    reminder_status_id INT REFERENCES reminder_status(reminder_status_id) DEFAULT 1
);

CREATE TABLE prescriptions (
    prescription_id SERIAL PRIMARY KEY,
    appointment_id INT NOT NULL REFERENCES appointments(appointment_id) ON DELETE CASCADE,
    doctor_id INT NOT NULL REFERENCES doctors(doctor_id),
    patient_id INT NOT NULL REFERENCES patients(patient_id),
    prescription_text TEXT NOT NULL,
    issued_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE doctor_reviews (
    review_id SERIAL PRIMARY KEY,
    doctor_id INT NOT NULL REFERENCES doctors(doctor_id),
    patient_id INT NOT NULL REFERENCES patients(patient_id),
    rating INT CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ------------------------------
-- Payments
-- ------------------------------

CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    appointment_id INT REFERENCES appointments(appointment_id) ON DELETE CASCADE,
    patient_id INT REFERENCES patients(patient_id),
    doctor_id INT REFERENCES doctors(doctor_id),
    amount NUMERIC(10,2) NOT NULL,
    method_id INT REFERENCES payment_methods(method_id),
    status_id INT REFERENCES payment_status(status_id),
    transaction_time TIMESTAMP DEFAULT NOW()
);

CREATE TABLE commissions (
    commission_id SERIAL PRIMARY KEY,
    payment_id INT REFERENCES payments(payment_id) ON DELETE CASCADE,
    admin_id INT REFERENCES admins(admin_id),
    commission_amount NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ------------------------------
-- Chat & Security
-- ------------------------------

CREATE TABLE chat_messages (
    message_id SERIAL PRIMARY KEY,
    appointment_id INT REFERENCES appointments(appointment_id) ON DELETE CASCADE,
    sender_id INT REFERENCES users(user_id),
    receiver_id INT REFERENCES users(user_id),
    message_text TEXT,
    sent_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE call_sessions (
    call_id SERIAL PRIMARY KEY,
    appointment_id INT REFERENCES appointments(appointment_id),
    doctor_id INT REFERENCES doctors(doctor_id),
    patient_id INT REFERENCES patients(patient_id),
    call_type VARCHAR(20) CHECK (call_type IN ('audio', 'video')),
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    duration INTERVAL
);

CREATE TABLE audit_logs (
    log_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    action VARCHAR(100),
    table_name VARCHAR(50),
    record_id INT,
    timestamp TIMESTAMP DEFAULT NOW(),
    details JSONB
);
