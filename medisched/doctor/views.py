from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DoctorExperience, Doctor,DoctorAppointmentFee

from adminapp.models import Division, District, Upazila, Department, Symptom
from .models import Doctor,DoctorSpecializationDepartment,DoctorSpecializationSymptom,DoctorExperience




@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, 'doctor_profile'):
        return redirect('/')  # Unauthorized access

    context = {
        'doctor_user': request.user,
        'upcoming_appointments_count': 5,
        'patients_today_count': 8,
        'earnings_today': 120,
        'total_reviews': 15,
        'upcoming_appointments': [
            {
                'patient': {'first_name': 'John', 'last_name': 'Doe'},
                'appointment_date': '2025-11-08',
                'appointment_time': '10:00 AM',
                'status': {'status_name': 'Pending'}
            },
        ]
    }
    return render(request, 'doctor/dashboard.html', context)


@login_required
def doctor_profile(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    context = {'doctor': doctor}
    return render(request, 'doctor/dashboard.html', context)


@login_required
def doctor_profile_edit(request):
    """Allow doctor to edit both User and Doctor profile info"""
    doctor, created = Doctor.objects.get_or_create(user=request.user)

    # Fetch dropdown options
    divisions = Division.objects.all()
    districts = District.objects.all()
    upazilas = Upazila.objects.all()
    departments = Department.objects.all()
    symptoms = Symptom.objects.all()

    if request.method == 'POST':
        # ---------- USER MODEL UPDATE ----------
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.save()

        # ---------- DOCTOR MODEL UPDATE ----------
        doctor.about = request.POST.get('about', doctor.about)
        doctor.qualification = request.POST.get('qualification', doctor.qualification)
        doctor.total_experience = request.POST.get('total_experience', doctor.total_experience)
        doctor.bmdc_number = request.POST.get('bmdc_number', doctor.bmdc_number)

        # ---------- Safe ForeignKey Assignment ----------
        division_id = request.POST.get('division')
        district_id = request.POST.get('district')
        upazila_id = request.POST.get('upazila')

        doctor.division = Division.objects.filter(id=division_id).first() if division_id else None
        doctor.district = District.objects.filter(id=district_id).first() if district_id else None
        doctor.upazila = Upazila.objects.filter(id=upazila_id).first() if upazila_id else None

        # ---------- Profile Image ----------
        if 'profile_image' in request.FILES:
            doctor.profile_image = request.FILES['profile_image']

        doctor.save()

        messages.success(request, "✅ Profile updated successfully!")
        return redirect('doctor:doctor_profile_edit')

    context = {
        'doctor': doctor,
        'divisions': divisions,
        'districts': districts,
        'upazilas': upazilas,
        'departments': departments,
        'symptoms': symptoms,
    }
    return render(request, 'doctor/profile_edit.html', context)




# Expertise section
@login_required
def doctor_expertise_edit(request):

    doctor = get_object_or_404(Doctor, user=request.user)

    departments = Department.objects.all()
    symptoms = Symptom.objects.all()

    # ✅ Doctor’s selected departments
    selected_departments = DoctorSpecializationDepartment.objects.filter(
        doctor=doctor
    ).values_list('department_id', flat=True)

    # ✅ Doctor’s selected symptoms
    selected_symptoms = DoctorSpecializationSymptom.objects.filter(
        doctor=doctor
    ).values_list('symptom_id', flat=True)

    context = {
        "doctor": doctor,
        "departments": departments,
        "symptoms": symptoms,
        "selected_departments": list(selected_departments),
        "selected_symptoms": list(selected_symptoms),
    }

    return render(request, "doctor/expertise_edit.html", context)

@login_required
def update_doctor_expertise(request):

    doctor = get_object_or_404(Doctor, user=request.user)

    if request.method == "POST":

        dept_ids = request.POST.getlist("departments[]")
        sym_ids = request.POST.getlist("symptoms[]")

        # ✅ clear old relations
        DoctorSpecializationDepartment.objects.filter(doctor=doctor).delete()
        DoctorSpecializationSymptom.objects.filter(doctor=doctor).delete()

        # ✅ add departments
        for d_id in dept_ids:
            DoctorSpecializationDepartment.objects.create(
                doctor=doctor,
                department_id=d_id
            )

        # ✅ add symptoms
        for s_id in sym_ids:
            DoctorSpecializationSymptom.objects.create(
                doctor=doctor,
                symptom_id=s_id
            )

        messages.success(request, "Your expertise has been updated successfully!")
        return redirect("doctor:expertise_edit")

    return redirect("doctor:expertise_edit")


# --- AJAX endpoints ---
@login_required
def ajax_load_districts(request):
    division_id = request.GET.get('division_id')
    districts = District.objects.filter(division_id=division_id).values('id', 'district_name')
    return JsonResponse(list(districts), safe=False)


@login_required
def ajax_load_upazilas(request):
    district_id = request.GET.get('district_id')
    upazilas = Upazila.objects.filter(district_id=district_id).values('id', 'upazila_name')
    return JsonResponse(list(upazilas), safe=False)





DAYS_OF_WEEK = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']


@login_required
def doctor_experience_manage(request, exp_id=None):
    doctor = get_object_or_404(Doctor, user=request.user)
    experiences = doctor.experiences.all()
    working_hours = doctor.working_hours or {}

    # For editing specific experience
    experience = None
    if exp_id:
        experience = get_object_or_404(DoctorExperience, id=exp_id, doctor=doctor)

    # ------------------------------
    #   WHEN ONLY WORKING HOURS SAVED
    # ------------------------------
    if request.method == "POST" and "working_hours_submit" in request.POST:
        updated_hours = {}
        for day in DAYS_OF_WEEK:
            time_value = request.POST.get(f"wh_{day}", "")
            updated_hours[day] = time_value

        doctor.working_hours = updated_hours
        doctor.save()
        messages.success(request, "Working hours updated successfully.")
        return redirect("doctor:experience_manage")

    # ------------------------------
    #   WHEN EXPERIENCE ADD / EDIT
    # ------------------------------
    if request.method == "POST" and "experience_submit" in request.POST:
        hospital_name = request.POST.get("hospital_name")
        designation = request.POST.get("designation")
        department = request.POST.get("department")

        if not hospital_name or not designation:
            messages.error(request, "Hospital name and designation are required.")
            return redirect("doctor:experience_manage")

        if experience:
            # Update
            experience.hospital_name = hospital_name
            experience.designation = designation
            experience.department = department
            experience.save()
            messages.success(request, "Experience updated successfully.")
        else:
            # Add
            DoctorExperience.objects.create(
                doctor=doctor,
                hospital_name=hospital_name,
                designation=designation,
                department=department,
            )
            messages.success(request, "Experience added successfully.")

        return redirect("doctor:experience_manage")

    context = {
        "experiences": experiences,
        "experience": experience,
        "days": DAYS_OF_WEEK,
        "working_hours": working_hours,
    }

    return render(request, "doctor/experience_manage.html", context)

@login_required
def doctor_experience_delete(request, exp_id):
    doctor = get_object_or_404(Doctor, user=request.user)
    experience = get_object_or_404(DoctorExperience, id=exp_id, doctor=doctor)
    experience.delete()
    messages.success(request, "Experience deleted successfully.")
    return redirect('doctor:experience_manage')



@login_required
def manage_appointment_fees(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    categories = [choice[0] for choice in DoctorAppointmentFee.APPOINTMENT_CATEGORIES]
    fees = {fee.category: fee for fee in doctor.appointment_fees.all()}

    if request.method == 'POST':
        for category in categories:
            price = request.POST.get(f'price_{category}')
            if price:
                # Update or create fee
                DoctorAppointmentFee.objects.update_or_create(
                    doctor=doctor,
                    category=category,
                    defaults={'price': price}
                )
            else:
                # Delete if empty
                DoctorAppointmentFee.objects.filter(doctor=doctor, category=category).delete()

        messages.success(request, "Appointment fees updated successfully!")
        return redirect('doctor:manage_appointment_fees')

    context = {
        'categories': DoctorAppointmentFee.APPOINTMENT_CATEGORIES,
        'fees': fees,
    }
    return render(request, 'doctor/manage_appointment_fees.html', context)