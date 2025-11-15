from django.shortcuts import render, redirect, get_object_or_404
from .models import Division, District, Upazila, Department, Symptom
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

# Dashboard
def admin_dashboard(request):
    return render(request, 'adminapp/admin_dashboard.html')


# ---------- Division ----------
def division_list(request):
    divisions = Division.objects.all()
    return render(request, 'adminapp/division_list.html', {'divisions': divisions})

def add_division(request):
    if request.method == 'POST':
        name = request.POST['division_name']
        Division.objects.create(division_name=name)
        messages.success(request, 'Division added successfully!')
        return redirect('division_list')
    return redirect('division_list')

def delete_division(request, id):
    division = get_object_or_404(Division, id=id)
    division.delete()
    messages.success(request, 'Division deleted!')
    return redirect('division_list')

def edit_division(request, id):
    division = get_object_or_404(Division, id=id)
    if request.method == 'POST':
        division_name = request.POST['division_name']
        division.division_name = division_name
        division.save()
        messages.success(request, 'Division updated successfully!')
        return redirect('division_list')
    return render(request, 'adminapp/edit_division.html', {'division': division})



# ---------- District ----------
def district_list(request):
    districts = District.objects.select_related('division').all()
    divisions = Division.objects.all()
    return render(request, 'adminapp/district_list.html', {'districts': districts, 'divisions': divisions})

def add_district(request):
    if request.method == 'POST':
        district_name = request.POST['district_name']
        division_id = request.POST['division_id']
        District.objects.create(district_name=district_name, division_id=division_id)
        messages.success(request, 'District added!')
        return redirect('district_list')
    return redirect('district_list')

def delete_district(request, id):
    district = get_object_or_404(District, id=id)
    district.delete()
    messages.success(request, 'District deleted!')
    return redirect('district_list')

def edit_district(request, id):
    district = get_object_or_404(District, id=id)
    divisions = Division.objects.all()
    if request.method == 'POST':
        district_name = request.POST['district_name']
        division_id = request.POST['division_id']
        district.district_name = district_name
        district.division_id = division_id
        district.save()
        messages.success(request, 'District updated successfully!')
        return redirect('district_list')
    return render(request, 'adminapp/edit_district.html', {'district': district, 'divisions': divisions})


# ---------- Upazila ----------
def upazila_list(request):
    upazilas = Upazila.objects.select_related('district').all()
    districts = District.objects.all()
    return render(request, 'adminapp/upazila_list.html', {'upazilas': upazilas, 'districts': districts})

def add_upazila(request):
    if request.method == 'POST':
        upazila_name = request.POST['upazila_name']
        district_id = request.POST['district_id']
        Upazila.objects.create(upazila_name=upazila_name, district_id=district_id)
        messages.success(request, 'Upazila added!')
        return redirect('upazila_list')
    return redirect('upazila_list')
def edit_upazila(request, id):
    upazila = get_object_or_404(Upazila, id=id)
    districts = District.objects.select_related('division').all()
    if request.method == 'POST':
        upazila_name = request.POST['upazila_name']
        district_id = request.POST['district_id']
        upazila.upazila_name = upazila_name
        upazila.district_id = district_id
        upazila.save()
        messages.success(request, 'Upazila updated successfully!')
        return redirect('upazila_list')
    return render(request, 'adminapp/edit_upazila.html', {'upazila': upazila, 'districts': districts})


def delete_upazila(request, id):
    upazila = get_object_or_404(Upazila, id=id)
    upazila.delete()
    messages.success(request, 'Upazila deleted!')
    return redirect('upazila_list')


# ---------- Department ----------
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'adminapp/department_list.html', {'departments': departments})

def add_department(request):
    if request.method == 'POST':
        name = request.POST.get('department_name')
        image = request.FILES.get('department_image')  # get uploaded image
        Department.objects.create(department_name=name, department_image=image)
        messages.success(request, 'Department added!')
        return redirect('department_list')
    return redirect('department_list')

def edit_department(request, id):
    department = get_object_or_404(Department, id=id)
    if request.method == 'POST':
        name = request.POST.get('department_name')
        image = request.FILES.get('department_image')  # get uploaded image (optional)

        department.department_name = name
        if image:  # only update if a new image is uploaded
            department.department_image = image

        department.save()
        messages.success(request, 'Department updated!')
        return redirect('department_list')

    return render(request, 'adminapp/edit_department.html', {'department': department})

def delete_department(request, id):
    department = get_object_or_404(Department, id=id)
    # Optional: delete image file from storage when deleting record
    if department.department_image:
        department.department_image.delete(save=False)
    department.delete()
    messages.success(request, 'Department deleted!')
    return redirect('department_list')



# ---------- Symptom List ----------
def symptom_list(request):
    symptoms = Symptom.objects.all()
    return render(request, 'adminapp/symptom_list.html', {'symptoms': symptoms})


# ---------- Add Symptom ----------
def add_symptom(request):
    if request.method == 'POST':
        name = request.POST.get('symptom_name')
        image = request.FILES.get('symptom_image')  # handle file upload

        # Create the new symptom record
        Symptom.objects.create(symptom_name=name, symptom_image=image)

        messages.success(request, 'Symptom added successfully!')
        return redirect('symptom_list')

    return redirect('symptom_list')


# ---------- Edit Symptom ----------
def edit_symptom(request, id):
    symptom = get_object_or_404(Symptom, id=id)

    if request.method == 'POST':
        name = request.POST.get('symptom_name')
        image = request.FILES.get('symptom_image')

        symptom.symptom_name = name

        # If a new image is uploaded, replace the old one
        if image:
            symptom.symptom_image = image

        symptom.save()
        messages.success(request, 'Symptom updated successfully!')
        return redirect('symptom_list')

    return render(request, 'adminapp/edit_symptom.html', {'symptom': symptom})


# ---------- Delete Symptom ----------
def delete_symptom(request, id):
    symptom = get_object_or_404(Symptom, id=id)
    symptom.delete()
    messages.success(request, 'Symptom deleted successfully!')
    return redirect('symptom_list')



def appointment_list(request):
    # fetch appointments from database
    appointments = []  # replace with actual query
    return render(request, 'adminapp/appointment_list.html', {'appointments': appointments})


# Payments
def payment_list(request):
    # Fetch all payments (example)
    # from payments.models import Payment  # if you have payments app
    payments = []  # replace with real query
    return render(request, 'adminapp/payment_list.html', {'payments': payments})



def user_logout(request):
    logout(request)
    return redirect('login')  # Replace 'login' with your login page URL name


