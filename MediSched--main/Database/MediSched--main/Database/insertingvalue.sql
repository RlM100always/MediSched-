-- ==============================
-- LOOKUP TABLES DATA
-- ==============================

-- Roles
INSERT INTO roles (role_name) VALUES
('patient'),
('doctor'),
('admin');

-- Genders
INSERT INTO genders (gender_name) VALUES
('Male'),
('Female'),
('Other');

-- Appointment Status
INSERT INTO appointment_status (status_name) VALUES
('Pending'),
('Confirmed'),
('Completed'),
('Cancelled'),
('No Show');

-- Reminder Types
INSERT INTO reminder_types (type_name) VALUES
('SMS'),
('Email'),
('Push Notification'),
('WhatsApp');

-- Reminder Status
INSERT INTO reminder_status (status_name) VALUES
('Pending'),
('Sent'),
('Failed'),
('Delivered');

-- Payment Methods
INSERT INTO payment_methods (method_name) VALUES
('bKash'),
('Nagad'),
('Rocket'),
('Credit Card'),
('Debit Card'),
('Bank Transfer'),
('Cash');

-- Payment Status
INSERT INTO payment_status (status_name) VALUES
('Pending'),
('Completed'),
('Failed'),
('Refunded');

-- Blood Groups
INSERT INTO blood_group (blood_group_name) VALUES
('A+'),
('A-'),
('B+'),
('B-'),
('O+'),
('O-'),
('AB+'),
('AB-');

-- ------------------------------
-- Divisions
-- ------------------------------
INSERT INTO divisions (division_name) VALUES
('Dhaka'),
('Chattogram'),
('Rajshahi'),
('Khulna'),
('Barishal'),
('Sylhet'),
('Rangpur'),
('Mymensingh');

-- ------------------------------
-- Districts
-- ------------------------------
-- Dhaka Division
INSERT INTO districts (district_name, division_id) VALUES
('Dhaka', 1),
('Gazipur', 1),
('Narayanganj', 1),
('Tangail', 1),
('Munshiganj', 1),
('Manikganj', 1),
('Madaripur', 1),
('Shariatpur', 1),
('Munshiganj', 1),
('Narsingdi', 1);

-- Chattogram Division
INSERT INTO districts (district_name, division_id) VALUES
('Chattogram', 2),
('Cox''s Bazar', 2),
('Cumilla', 2),
('Feni', 2),
('Khagrachari', 2),
('Lakshmipur', 2),
('Noakhali', 2),
('Brahmanbaria', 2),
('Chandpur', 2),
('Chattogram', 2);

-- Rajshahi Division
INSERT INTO districts (district_name, division_id) VALUES
('Rajshahi', 3),
('Bogura', 3),
('Naogaon', 3),
('Chapainawabganj', 3),
('Pabna', 3),
('Sirajganj', 3),
('Natore', 3),
('Joypurhat', 3),
('Kushtia', 3),
('Meherpur', 3);

-- Khulna Division
INSERT INTO districts (district_name, division_id) VALUES
('Khulna', 4),
('Jessore', 4),
('Satkhira', 4),
('Kushtia', 4),
('Chuadanga', 4),
('Magura', 4),
('Narail', 4),
('Meherpur', 4),
('Jhenaidah', 4),
('Bagerhat', 4);

-- Barishal Division
INSERT INTO districts (district_name, division_id) VALUES
('Barishal', 5),
('Bhola', 5),
('Patuakhali', 5),
('Pirojpur', 5),
('Jhalokathi', 5),
('Barguna', 5);

-- Sylhet Division
INSERT INTO districts (district_name, division_id) VALUES
('Sylhet', 6),
('Moulvibazar', 6),
('Sunamganj', 6),
('Habiganj', 6);

-- Rangpur Division
INSERT INTO districts (district_name, division_id) VALUES
('Rangpur', 7),
('Kurigram', 7),
('Gaibandha', 7),
('Nilphamari', 7),
('Lalmonirhat', 7),
('Kochbihar', 7),
('Dinajpur', 7),
('Thakurgaon', 7),
('Panchagarh', 7);

-- Mymensingh Division
INSERT INTO districts (district_name, division_id) VALUES
('Mymensingh', 8),
('Jamalpur', 8),
('Sherpur', 8),
('Netrokona', 8),
('Kishoreganj', 8);

-- ------------------------------
-- Upazilas
-- ------------------------------
-- Dhaka District
INSERT INTO upazilas (upazila_name, district_id) VALUES
('Dhamrai', 1),
('Dohar', 1),
('Keraniganj', 1),
('Narayanganj Sadar', 1),
('Gulshan', 1),
('Mirpur', 1),
('Gajipur Sadar', 1),
('Narayanganj', 1),
('Dohar', 1),
('Keraniganj', 1);

-- Chattogram District
INSERT INTO upazilas (upazila_name, district_id) VALUES
('Mirsharai', 2),
('Fatikchhari', 2),
('Sandwip', 2),
('Sitakunda', 2),
('Hathazari', 2),
('Raozan', 2),
('Rangunia', 2),
('Karnaphuli', 2),
('Boalkhali', 2),
('Patiya', 2);

-- Rajshahi District
INSERT INTO upazilas (upazila_name, district_id) VALUES
('Rajshahi Sadar', 3),
('Bogura Sadar', 3),
('Naogaon Sadar', 3),
('Chapainawabganj Sadar', 3),
('Pabna Sadar', 3),
('Sirajganj Sadar', 3),
('Natore Sadar', 3),
('Joypurhat Sadar', 3),
('Kushtia Sadar', 3),
('Meherpur Sadar', 3);

-- Khulna District
INSERT INTO upazilas (upazila_name, district_id) VALUES
('Khulna Sadar', 4),
('Jessore Sadar', 4),
('Satkhira Sadar', 4),
('Kushtia Sadar', 4),
('Chuadanga Sadar', 4),
('Magura Sadar', 4),
('Narail Sadar', 4),
('Meherpur Sadar', 4),
('Jhenaidah Sadar', 4),
('Bagerhat Sadar', 4);

-- Barishal District
INSERT INTO upazilas (upazila_name, district_id) VALUES
('Barishal Sadar', 5),
('Bhola Sadar', 5),
('Patuakhali Sadar', 5),
('Pirojpur Sadar', 5),
('Jhalokathi Sadar', 5),
('Barguna Sadar', 5);

-- Sylhet District
INSERT INTO upazilas (upazila_name, district_id) VALUES
('Sylhet Sadar', 6),
('Moulvibazar Sadar', 6),
('Sunamganj Sadar', 6),
('Habiganj Sadar', 6);

-- Rangpur District
INSERT INTO upazilas (upazila_name, district_id) VALUES
('Rangpur Sadar', 7),
('Kurigram Sadar', 7),
('Gaibandha Sadar', 7),
('Nilphamari Sadar', 7),
('Lalmonirhat Sadar', 7),
('Kochbihar Sadar', 7),
('Dinajpur Sadar', 7),
('Thakurgaon Sadar', 7),
('Panchagarh Sadar', 7);

-- Mymensingh District
INSERT INTO upazilas (upazila_name, district_id) VALUES
('Mymensingh Sadar', 8),
('Jamalpur Sadar', 8),
('Sherpur Sadar', 8),
('Netrokona Sadar', 8),
('Kishoreganj Sadar', 8);


-- Symptoms
INSERT INTO symptoms (symptom_name, symptom_image) VALUES
('Fever', 'fever.png'),
('Headache', 'headache.png'),
('Cough', 'cough.png'),
('Cold', 'cold.png'),
('Stomach Pain', 'stomach_pain.png'),
('Chest Pain', 'chest_pain.png'),
('Back Pain', 'back_pain.png'),
('Diabetes', 'diabetes.png'),
('High Blood Pressure', 'hypertension.png'),
('Skin Rash', 'skin_rash.png'),
('Dizziness', 'dizziness.png'),
('Fatigue', 'fatigue.png');

-- Departments
INSERT INTO departments (department_name, department_image) VALUES
('General Medicine', 'general_medicine.png'),
('Cardiology', 'cardiology.png'),
('Pediatrics', 'pediatrics.png'),
('Dermatology', 'dermatology.png'),
('Orthopedics', 'orthopedics.png'),
('Neurology', 'neurology.png'),
('Gynecology', 'gynecology.png'),
('Psychiatry', 'psychiatry.png'),
('ENT', 'ent.png'),
('Ophthalmology', 'ophthalmology.png'),
('Dentistry', 'dentistry.png'),
('Gastroenterology', 'gastroenterology.png');

-- ==============================
-- USERS DATA
-- ==============================

-- Admin Users
INSERT INTO users (first_name, last_name, email, password_hash, phone, role_id) VALUES
('Rakib', 'Hasan', 'admin@telemedicine.bd', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801712345678', 3);

-- Doctor Users
INSERT INTO users (first_name, last_name, email, password_hash, phone, role_id) VALUES
('Dr. Farhan', 'Ahmed', 'farhan.ahmed@doctor.bd', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801712345679', 2),
('Dr. Nusrat', 'Jahan', 'nusrat.jahan@doctor.bd', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801812345680', 2),
('Dr. Masud', 'Rana', 'masud.rana@doctor.bd', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801912345681', 2),
('Dr. Sabrina', 'Khan', 'sabrina.khan@doctor.bd', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801612345682', 2),
('Dr. Imran', 'Hossain', 'imran.hossain@doctor.bd', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801712345683', 2),
('Dr. Farhana', 'Islam', 'farhana.islam@doctor.bd', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801812345684', 2),
('Dr. Kamal', 'Uddin', 'kamal.uddin@doctor.bd', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801912345685', 2),
('Dr. Ayesha', 'Siddika', 'ayesha.siddika@doctor.bd', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801612345686', 2),
('Dr. Rashid', 'Mahmud', 'rashid.mahmud@doctor.bd', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801712345687', 2),
('Dr. Sultana', 'Begum', 'sultana.begum@doctor.bd', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801812345688', 2);

-- Patient Users
INSERT INTO users (first_name, last_name, email, password_hash, phone, role_id) VALUES
('Rashed', 'Islam', 'rashed.islam@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801712345689', 1),
('Tahmina', 'Akter', 'tahmina.akter@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801812345690', 1),
('Rubel', 'Hossain', 'rubel.hossain@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801912345691', 1),
('Sharmin', 'Sultana', 'sharmin.sultana@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801612345692', 1),
('Karim', 'Mia', 'karim.mia@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801712345693', 1),
('Nasrin', 'Akter', 'nasrin.akter@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801812345694', 1),
('Shahid', 'Ullah', 'shahid.ullah@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801912345695', 1),
('Moriam', 'Begum', 'moriam.begum@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801612345696', 1),
('Selim', 'Reza', 'selim.reza@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801712345697', 1),
('Fatema', 'Khatun', 'fatema.khatun@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801812345698', 1),
('Aziz', 'Rahman', 'aziz.rahman@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801912345699', 1),
('Rehana', 'Parveen', 'rehana.parveen@gmail.com', '$2b$10$abcdefghijklmnopqrstuvwxyz123456', '+8801612345700', 1);

-- ==============================
-- ADMIN DATA
-- ==============================

INSERT INTO admins (admin_id, role_description) VALUES
(1, 'System Administrator - Full access to platform management and configurations');

-- ==============================
-- DOCTORS DATA
-- ==============================

INSERT INTO doctors (doctor_id, about, bmdc_number, qualification, total_experience, working_hours, profile_image, is_verified, division_id, district_id, upazila_id) VALUES
(2, 'Experienced cardiologist specializing in heart disease treatment and prevention', 'BMDC-12345', 'MBBS, MD (Cardiology)', 12, '{"saturday": "09:00-17:00", "sunday": "09:00-17:00", "monday": "09:00-17:00", "tuesday": "09:00-17:00", "wednesday": "09:00-17:00", "thursday": "09:00-13:00"}', 'dr_farhan.jpg', TRUE, 1, 1, 1),
(3, 'Pediatric specialist with focus on child healthcare and immunization', 'BMDC-12346', 'MBBS, DCH, FCPS (Pediatrics)', 10, '{"saturday": "10:00-18:00", "sunday": "10:00-18:00", "monday": "10:00-18:00", "tuesday": "10:00-18:00", "wednesday": "10:00-18:00"}', 'dr_nusrat.jpg', TRUE, 1, 1, 2),
(4, 'General medicine practitioner with extensive experience in treating common ailments', 'BMDC-12347', 'MBBS, FCPS (Medicine)', 15, '{"saturday": "08:00-16:00", "sunday": "08:00-16:00", "monday": "08:00-16:00", "tuesday": "08:00-16:00", "wednesday": "08:00-16:00", "thursday": "08:00-12:00"}', 'dr_masud.jpg', TRUE, 2, 4, 6),
(5, 'Dermatologist specializing in skin, hair, and nail disorders', 'BMDC-12348', 'MBBS, DDV, MD (Dermatology)', 8, '{"sunday": "09:00-17:00", "monday": "09:00-17:00", "tuesday": "09:00-17:00", "wednesday": "09:00-17:00", "thursday": "09:00-17:00"}', 'dr_sabrina.jpg', TRUE, 1, 1, 1),
(6, 'Orthopedic surgeon expert in bone and joint treatments', 'BMDC-12349', 'MBBS, MS (Orthopedics)', 14, '{"saturday": "10:00-18:00", "sunday": "10:00-18:00", "monday": "10:00-18:00", "wednesday": "10:00-18:00", "thursday": "10:00-18:00"}', 'dr_imran.jpg', TRUE, 3, 6, 8),
(7, 'Gynecologist providing comprehensive women healthcare services', 'BMDC-12350', 'MBBS, FCPS (Gynecology & Obstetrics)', 11, '{"saturday": "09:00-17:00", "sunday": "09:00-17:00", "monday": "09:00-17:00", "tuesday": "09:00-17:00", "thursday": "09:00-17:00"}', 'dr_farhana.jpg', TRUE, 1, 2, 4),
(8, 'Neurologist specializing in brain and nervous system disorders', 'BMDC-12351', 'MBBS, MD (Neurology)', 9, '{"sunday": "10:00-18:00", "monday": "10:00-18:00", "tuesday": "10:00-18:00", "wednesday": "10:00-18:00", "thursday": "10:00-18:00"}', 'dr_kamal.jpg', TRUE, 4, 8, 10),
(9, 'Psychiatrist providing mental health counseling and treatment', 'BMDC-12352', 'MBBS, MPhil (Psychiatry)', 7, '{"saturday": "11:00-19:00", "sunday": "11:00-19:00", "monday": "11:00-19:00", "tuesday": "11:00-19:00", "wednesday": "11:00-19:00"}', 'dr_ayesha.jpg', TRUE, 1, 1, 2),
(10, 'ENT specialist treating ear, nose, and throat conditions', 'BMDC-12353', 'MBBS, FCPS (ENT)', 13, '{"saturday": "08:00-16:00", "sunday": "08:00-16:00", "monday": "08:00-16:00", "tuesday": "08:00-16:00", "wednesday": "08:00-16:00"}', 'dr_rashid.jpg', TRUE, 6, 11, 13),
(11, 'Gastroenterologist expert in digestive system disorders', 'BMDC-12354', 'MBBS, MD (Gastroenterology)', 10, '{"sunday": "09:00-17:00", "monday": "09:00-17:00", "tuesday": "09:00-17:00", "wednesday": "09:00-17:00", "thursday": "09:00-17:00"}', 'dr_sultana.jpg', TRUE, 1, 3, 5);

-- ==============================
-- DOCTOR EXPERIENCE
-- ==============================

INSERT INTO doctor_experience (doctor_id, hospital_name, designation, department) VALUES
(2, 'Square Hospital', 'Senior Consultant', 'Cardiology'),
(2, 'United Hospital', 'Consultant', 'Cardiology'),
(3, 'Bangladesh Shishu Hospital', 'Senior Pediatrician', 'Pediatrics'),
(3, 'Apollo Hospital Dhaka', 'Consultant', 'Pediatrics'),
(4, 'Dhaka Medical College Hospital', 'Associate Professor', 'Medicine'),
(4, 'Labaid Hospital', 'Senior Consultant', 'General Medicine'),
(5, 'Bangabandhu Sheikh Mujib Medical University', 'Assistant Professor', 'Dermatology'),
(5, 'Popular Medical College Hospital', 'Consultant', 'Dermatology'),
(6, 'National Orthopaedic Hospital', 'Senior Consultant', 'Orthopedics'),
(6, 'Evercare Hospital Dhaka', 'Consultant', 'Orthopedics'),
(7, 'Ad-din Women''s Medical College Hospital', 'Senior Consultant', 'Gynecology'),
(8, 'National Institute of Neurosciences', 'Consultant', 'Neurology'),
(9, 'National Institute of Mental Health', 'Associate Professor', 'Psychiatry'),
(10, 'Holy Family Red Crescent Hospital', 'Senior Consultant', 'ENT'),
(11, 'Ibrahim Cardiac Hospital', 'Consultant', 'Gastroenterology');

-- ==============================
-- DOCTOR SPECIALIZATIONS
-- ==============================

INSERT INTO doctor_specialization_departments (doctor_id, department_id) VALUES
(2, 2),  -- Dr. Farhan - Cardiology
(3, 3),  -- Dr. Nusrat - Pediatrics
(4, 1),  -- Dr. Masud - General Medicine
(5, 4),  -- Dr. Sabrina - Dermatology
(6, 5),  -- Dr. Imran - Orthopedics
(7, 7),  -- Dr. Farhana - Gynecology
(8, 6),  -- Dr. Kamal - Neurology
(9, 8),  -- Dr. Ayesha - Psychiatry
(10, 9), -- Dr. Rashid - ENT
(11, 12); -- Dr. Sultana - Gastroenterology

INSERT INTO doctor_specialization_symptoms (doctor_id, symptom_id) VALUES
(2, 6),  -- Dr. Farhan - Chest Pain
(2, 9),  -- Dr. Farhan - High Blood Pressure
(3, 1),  -- Dr. Nusrat - Fever
(3, 3),  -- Dr. Nusrat - Cough
(4, 1),  -- Dr. Masud - Fever
(4, 2),  -- Dr. Masud - Headache
(4, 12), -- Dr. Masud - Fatigue
(5, 10), -- Dr. Sabrina - Skin Rash
(6, 7),  -- Dr. Imran - Back Pain
(7, 5),  -- Dr. Farhana - Stomach Pain
(8, 2),  -- Dr. Kamal - Headache
(8, 11), -- Dr. Kamal - Dizziness
(9, 2),  -- Dr. Ayesha - Headache
(10, 4), -- Dr. Rashid - Cold
(11, 5); -- Dr. Sultana - Stomach Pain

-- ==============================
-- PATIENTS DATA
-- ==============================

INSERT INTO patients (patient_id, date_of_birth, gender_id, division_id, district_id, upazila_id, exact_location, blood_group_id, medical_history) VALUES
(12, '1985-03-15', 1, 1, 1, 1, 'House 12, Road 5, Dhanmondi', 1, 'History of hypertension'),
(13, '1990-07-22', 2, 1, 1, 2, 'Flat 4B, Gulshan Avenue, Gulshan-2', 3, 'No significant medical history'),
(14, '1978-11-30', 1, 1, 1, 3, 'Mirpur-10, Section C', 5, 'Diabetes Type 2 diagnosed in 2015'),
(15, '1995-05-18', 2, 1, 2, 4, 'Gazipur Chowrasta, Gazipur Sadar', 2, 'Asthma since childhood'),
(16, '1982-09-08', 1, 2, 4, 6, 'Agrabad, Chattogram', 1, 'Previous surgery for appendicitis'),
(17, '1988-12-25', 2, 1, 3, 5, 'Narayanganj Sadar', 4, 'Allergic to penicillin'),
(18, '1975-06-14', 1, 3, 6, 8, 'Shaheb Bazar, Rajshahi', 3, 'Chronic back pain'),
(19, '1992-02-28', 2, 1, 1, 1, 'Bashundhara R/A, Block D', 6, 'No significant medical history'),
(20, '1980-10-05', 1, 4, 8, 10, 'Khulna Sadar', 1, 'History of acid reflux'),
(21, '1998-08-19', 2, 6, 11, 13, 'Sylhet Sadar', 2, 'No significant medical history'),
(22, '1987-04-12', 1, 1, 1, 2, 'Banani DOHS', 5, 'High cholesterol'),
(23, '1993-01-07', 2, 1, 1, 3, 'Mohammadpur, Dhaka', 7, 'Migraine episodes');

-- ==============================
-- APPOINTMENTS DATA
-- ==============================

INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status_id, reason, created_at) VALUES
(12, 2, '2025-10-26', '10:00:00', 2, 'Chest pain and irregular heartbeat', '2025-10-20 14:30:00'),
(13, 3, '2025-10-26', '11:00:00', 2, 'Child vaccination consultation', '2025-10-21 09:15:00'),
(14, 4, '2025-10-27', '09:00:00', 2, 'Diabetes follow-up and blood sugar management', '2025-10-22 16:45:00'),
(15, 5, '2025-10-27', '14:00:00', 1, 'Skin rash and itching problem', '2025-10-23 11:20:00'),
(16, 6, '2025-10-28', '10:30:00', 2, 'Knee pain and difficulty walking', '2025-10-23 13:00:00'),
(17, 7, '2025-10-28', '15:00:00', 1, 'Pregnancy check-up', '2025-10-24 10:30:00'),
(18, 8, '2025-10-29', '11:00:00', 2, 'Severe headache and dizziness', '2025-10-24 15:00:00'),
(19, 9, '2025-10-29', '16:00:00', 1, 'Anxiety and sleep disorder', '2025-10-25 08:45:00'),
(20, 10, '2025-10-30', '09:30:00', 2, 'Ear infection and hearing problem', '2025-10-25 12:00:00'),
(21, 11, '2025-10-30', '14:00:00', 1, 'Stomach pain and indigestion', '2025-10-25 14:30:00'),
(22, 2, '2025-11-01', '11:00:00', 1, 'High blood pressure consultation', '2025-10-25 16:00:00'),
(23, 4, '2025-11-02', '10:00:00', 1, 'Persistent fever and body ache', '2025-10-25 17:30:00');

-- ==============================
-- REMINDERS DATA
-- ==============================

INSERT INTO reminders (appointment_id, user_id, reminder_type_id, message, sent_at, reminder_status_id) VALUES
(1, 12, 1, 'Reminder: Your appointment with Dr. Farhan Ahmed is tomorrow at 10:00 AM', '2025-10-25 10:00:00', 2),
(1, 12, 2, 'Appointment Reminder: Tomorrow at 10:00 AM with Dr. Farhan Ahmed, Cardiology', '2025-10-25 10:05:00', 2),
(2, 13, 1, 'Reminder: Your appointment with Dr. Nusrat Jahan is tomorrow at 11:00 AM', '2025-10-25 11:00:00', 2),
(3, 14, 3, 'Upcoming appointment on Oct 27 at 09:00 AM with Dr. Masud Rana', '2025-10-26 09:00:00', 2),
(4, 15, 1, 'Your appointment with Dr. Sabrina Khan is scheduled for tomorrow at 2:00 PM', '2025-10-26 14:00:00', 1),
(5, 16, 2, 'Appointment reminder: Oct 28 at 10:30 AM with Dr. Imran Hossain', '2025-10-27 10:30:00', 1),
(6, 17, 1, 'Reminder: Appointment with Dr. Farhana Islam tomorrow at 3:00 PM', '2025-10-27 15:00:00', 1),
(7, 18, 4, 'Your appointment is scheduled for Oct 29 at 11:00 AM with Dr. Kamal Uddin', '2025-10-28 11:00:00', 1),
(8, 19, 1, 'Appointment reminder: Tomorrow at 4:00 PM with Dr. Ayesha Siddika', '2025-10-28 16:00:00', 1),
(9, 20, 2, 'Reminder: Your appointment is on Oct 30 at 09:30 AM with Dr. Rashid Mahmud', '2025-10-29 09:30:00', 1),
(10, 21, 3, 'Upcoming appointment: Oct 30 at 2:00 PM with Dr. Sultana Begum', '2025-10-29 14:00:00', 1),
(11, 22, 1, 'Your appointment with Dr. Farhan Ahmed is on Nov 1 at 11:00 AM', '2025-10-31 11:00:00', 1);

-- ==============================
-- PRESCRIPTIONS DATA
-- ==============================

INSERT INTO prescriptions (appointment_id, doctor_id, patient_id, prescription_text, issued_at) VALUES
(1, 2, 12, 'Rx: Tab. Atenolol 50mg - 1+0+1 (after meal), Tab. Aspirin 75mg - 0+0+1 (after meal), ECG and Echo recommended. Follow-up after 2 weeks.', '2025-10-26 10:45:00'),
(2, 3, 13, 'Rx: Vaccine: Pentavalent 3rd dose administered. Next vaccine due: MMR at 9 months. Continue vitamin D drops.', '2025-10-26 11:30:00'),
(3, 4, 14, 'Rx: Tab. Metformin 500mg - 1+0+1 (after meal), Blood sugar monitoring advised. Diet plan: Low carb, avoid sugar. Exercise 30 mins daily.', '2025-10-27 09:45:00'),
(5, 6, 16, 'Rx: Tab. Naproxen 500mg - 1+0+1 (after meal) for 7 days, Physiotherapy sessions recommended. Avoid heavy lifting. X-ray report reviewed.', '2025-10-28 11:15:00'),
(7, 8, 18, 'Rx: Tab. Propranolol 40mg - 1+0+1 for migraine prevention, MRI Brain ordered. Avoid stress and bright lights. Follow-up in 1 month.', '2025-10-29 11:45:00'),
(9, 10, 20, 'Rx: Ear drops: Ciprofloxacin + Dexamethasone - 3 drops 3 times daily for 7 days, Keep ear dry. Avoid water contact.', '2025-10-30 10:00:00');

-- ==============================
-- DOCTOR REVIEWS DATA
-- ==============================

INSERT INTO doctor_reviews (doctor_id, patient_id, rating, review_text, created_at) VALUES
(2, 12, 5, 'Excellent doctor! Very thorough examination and explained everything clearly. Highly recommended for heart problems.', '2025-10-26 12:00:00'),
(3, 13, 5, 'Dr. Nusrat is very caring and patient with children. My child felt comfortable during the entire visit.', '2025-10-26 13:30:00'),
(4, 14, 4, 'Good consultation. Dr. Masud provided detailed diet plan and medication instructions for diabetes management.', '2025-10-27 10:30:00'),
(6, 16, 5, 'Very experienced orthopedic surgeon. Diagnosed the problem accurately and provided effective treatment.', '2025-10-28 12:00:00'),
(8, 18, 5, 'Dr. Kamal is an excellent neurologist. He listened carefully to all symptoms and provided proper diagnosis.', '2025-10-29 13:00:00'),
(10, 20, 4, 'Professional and knowledgeable ENT specialist. Treatment was effective and recovery was quick.', '2025-10-30 11:00:00'),
(2, 22, 5, 'Best cardiologist in Dhaka. His treatment plan helped me control my blood pressure effectively.', '2025-10-20 15:00:00'),
(4, 23, 4, 'Dr. Masud is very experienced. He prescribed the right medicines and I felt better within days.', '2025-10-18 16:00:00'),
(5, 15, 5, 'Great dermatologist! Skin problem resolved completely after following her treatment plan.', '2025-10-15 14:00:00'),
(7, 17, 5, 'Dr. Farhana is very professional and caring. She made me feel comfortable during pregnancy consultation.', '2025-10-12 17:00:00');

-- ==============================
-- PAYMENTS DATA
-- ==============================

INSERT INTO payments (appointment_id, patient_id, doctor_id, amount, method_id, status_id, transaction_time) VALUES
(1, 12, 2, 1500.00, 1, 2, '2025-10-20 14:35:00'),
(2, 13, 3, 1200.00, 2, 2, '2025-10-21 09:20:00'),
(3, 14, 4, 1000.00, 1, 2, '2025-10-22 16:50:00'),
(4, 15, 5, 1300.00, 3, 1, '2025-10-23 11:25:00'),
(5, 16, 6, 1800.00, 1, 2, '2025-10-23 13:05:00'),
(6, 17, 7, 1400.00, 2, 1, '2025-10-24 10:35:00'),
(7, 18, 8, 2000.00, 4, 2, '2025-10-24 15:05:00'),
(8, 19, 9, 1600.00, 1, 1, '2025-10-25 08:50:00'),
(9, 20, 10, 1100.00, 2, 2, '2025-10-25 12:05:00'),
(10, 21, 11, 1500.00, 1, 1, '2025-10-25 14:35:00'),
(11, 22, 2, 1500.00, 3, 1, '2025-10-25 16:05:00'),
(12, 23, 4, 1000.00, 1, 1, '2025-10-25 17:35:00');

-- ==============================
-- COMMISSIONS DATA
-- ==============================

INSERT INTO commissions (payment_id, admin_id, commission_amount, created_at) VALUES
(1, 1, 150.00, '2025-10-20 14:36:00'),
(2, 1, 120.00, '2025-10-21 09:21:00'),
(3, 1, 100.00, '2025-10-22 16:51:00'),
(5, 1, 180.00, '2025-10-23 13:06:00'),
(7, 1, 200.00, '2025-10-24 15:06:00'),
(9, 1, 110.00, '2025-10-25 12:06:00');

-- ==============================
-- CHAT MESSAGES DATA
-- ==============================

INSERT INTO chat_messages (appointment_id, sender_id, receiver_id, message_text, sent_at) VALUES
(1, 12, 2, 'Good morning Doctor. I have been experiencing chest pain since yesterday.', '2025-10-26 09:45:00'),
(1, 2, 12, 'Good morning. Please describe the pain. Is it sharp or dull? Does it radiate?', '2025-10-26 09:47:00'),
(1, 12, 2, 'It is a dull ache in the center of my chest, sometimes spreads to left arm.', '2025-10-26 09:50:00'),
(1, 2, 12, 'I understand. Please take rest and avoid any strenuous activity. See you at 10 AM.', '2025-10-26 09:52:00'),
(2, 13, 3, 'Hello Doctor, my baby is 6 months old. Is it time for vaccination?', '2025-10-26 10:50:00'),
(2, 3, 13, 'Yes, your baby is due for Pentavalent 3rd dose. Please bring the vaccination card.', '2025-10-26 10:52:00'),
(3, 14, 4, 'Doctor, my blood sugar was 280 this morning. Should I be worried?', '2025-10-27 08:45:00'),
(3, 4, 14, 'That is quite high. Have you been following the diet plan? We will adjust medication today.', '2025-10-27 08:48:00'),
(5, 16, 6, 'Doctor, the knee pain is worse when I climb stairs.', '2025-10-28 10:15:00'),
(5, 6, 16, 'That indicates possible cartilage wear. We will do an X-ray and discuss treatment options.', '2025-10-28 10:18:00'),
(7, 18, 8, 'I have been having severe headaches for the past week, especially in the morning.', '2025-10-29 10:45:00'),
(7, 8, 18, 'Morning headaches can have various causes. I will examine you and may order an MRI.', '2025-10-29 10:47:00'),
(9, 20, 10, 'My right ear is blocked and I cannot hear properly from that side.', '2025-10-30 09:15:00'),
(9, 10, 20, 'It could be wax buildup or infection. I will examine your ear during the consultation.', '2025-10-30 09:18:00');

-- ==============================
-- CALL SESSIONS DATA
-- ==============================

INSERT INTO call_sessions (appointment_id, doctor_id, patient_id, call_type, started_at, ended_at, duration) VALUES
(1, 2, 12, 'video', '2025-10-26 10:00:00', '2025-10-26 10:25:00', '00:25:00'),
(2, 3, 13, 'video', '2025-10-26 11:00:00', '2025-10-26 11:20:00', '00:20:00'),
(3, 4, 14, 'video', '2025-10-27 09:00:00', '2025-10-27 09:35:00', '00:35:00'),
(5, 6, 16, 'video', '2025-10-28 10:30:00', '2025-10-28 11:00:00', '00:30:00'),
(7, 8, 18, 'video', '2025-10-29 11:00:00', '2025-10-29 11:30:00', '00:30:00'),
(9, 10, 20, 'video', '2025-10-30 09:30:00', '2025-10-30 09:55:00', '00:25:00'),
(1, 2, 12, 'audio', '2025-10-25 15:00:00', '2025-10-25 15:10:00', '00:10:00'),
(3, 4, 14, 'audio', '2025-10-26 18:00:00', '2025-10-26 18:08:00', '00:08:00'),
(5, 6, 16, 'audio', '2025-10-27 20:00:00', '2025-10-27 20:12:00', '00:12:00'),
(7, 8, 18, 'audio', '2025-10-28 19:30:00', '2025-10-28 19:45:00', '00:15:00');

-- ==============================
-- AUDIT LOGS DATA
-- ==============================

INSERT INTO audit_logs (user_id, action, table_name, record_id, timestamp, details) VALUES
(1, 'CREATE', 'users', 12, '2025-10-15 10:00:00', '{"action": "New patient registration", "email": "rashed.islam@gmail.com"}'),
(1, 'CREATE', 'users', 13, '2025-10-16 11:30:00', '{"action": "New patient registration", "email": "tahmina.akter@gmail.com"}'),
(2, 'UPDATE', 'doctors', 2, '2025-10-18 14:00:00', '{"action": "Updated working hours", "field": "working_hours"}'),
(1, 'CREATE', 'appointments', 1, '2025-10-20 14:30:00', '{"patient_id": 12, "doctor_id": 2, "date": "2025-10-26"}'),
(1, 'UPDATE', 'appointments', 1, '2025-10-21 09:00:00', '{"action": "Appointment confirmed", "status": "Confirmed"}'),
(2, 'CREATE', 'prescriptions', 1, '2025-10-26 10:45:00', '{"appointment_id": 1, "patient_id": 12}'),
(12, 'CREATE', 'doctor_reviews', 1, '2025-10-26 12:00:00', '{"doctor_id": 2, "rating": 5}'),
(1, 'CREATE', 'payments', 1, '2025-10-20 14:35:00', '{"amount": 1500.00, "method": "bKash", "status": "Completed"}'),
(1, 'CREATE', 'commissions', 1, '2025-10-20 14:36:00', '{"payment_id": 1, "amount": 150.00}'),
(3, 'UPDATE', 'doctors', 3, '2025-10-22 10:00:00', '{"action": "Profile updated", "field": "about"}'),
(1, 'CREATE', 'appointments', 7, '2025-10-24 15:00:00', '{"patient_id": 18, "doctor_id": 8, "date": "2025-10-29"}'),
(8, 'CREATE', 'prescriptions', 5, '2025-10-29 11:45:00', '{"appointment_id": 7, "patient_id": 18}'),
(1, 'UPDATE', 'users', 5, '2025-10-25 09:00:00', '{"action": "Password changed", "user_id": 5}'),
(1, 'CREATE', 'call_sessions', 1, '2025-10-26 10:00:00', '{"appointment_id": 1, "call_type": "video", "duration": "25 minutes"}');

-- ==============================
-- VERIFICATION QUERIES
-- ==============================
-- Run these queries to verify all data has been inserted correctly

-- SELECT COUNT(*) FROM roles;
-- SELECT COUNT(*) FROM users;
-- SELECT COUNT(*) FROM patients;
-- SELECT COUNT(*) FROM doctors;
-- SELECT COUNT(*) FROM appointments;
-- SELECT COUNT(*) FROM prescriptions;
-- SELECT COUNT(*) FROM payments;
-- SELECT COUNT(*) FROM doctor_reviews;
-- SELECT COUNT(*) FROM chat_messages;
-- SELECT COUNT(*) FROM call_sessions;
-- SELECT COUNT(*) FROM audit_logs;