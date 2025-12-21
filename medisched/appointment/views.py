from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal
import uuid

from doctor.models import Doctor, DoctorAppointmentFee
from .models import Appointment, PaymentTransaction
from .forms import AppointmentForm, PaymentMethodForm
@login_required
def book_appointment(request, doctor_id):
    """Step 1: Book appointment with doctor"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    # Get doctor's fees
    try:
        general_fee = DoctorAppointmentFee.objects.get(doctor=doctor, category='General').price
    except DoctorAppointmentFee.DoesNotExist:
        general_fee = Decimal('500.00')
    
    try:
        special_fee = DoctorAppointmentFee.objects.get(doctor=doctor, category='Special').price
    except DoctorAppointmentFee.DoesNotExist:
        special_fee = Decimal('1000.00')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor
            
            # Set consultation fee based on type
            consultation_type = form.cleaned_data['consultation_type']
            if consultation_type == 'general':
                appointment.consultation_fee = general_fee
            else:
                appointment.consultation_fee = special_fee
            
            # Calculate total amount
            vat_amount = appointment.consultation_fee * Decimal('0.05')
            appointment.vat_amount = vat_amount
            appointment.total_amount = appointment.consultation_fee + vat_amount + Decimal('29.00')
            
            appointment.save()
            
            # Store appointment ID in session for payment
            request.session['appointment_id'] = appointment.id
            
            messages.success(request, 'Please proceed to payment to confirm your appointment.')
            return redirect('appointment:payment')
    else:
        form = AppointmentForm()
    
    context = {
        'doctor': doctor,
        'form': form,
        'general_fee': general_fee,
        'special_fee': special_fee,
    }
    return render(request, 'appointment/book_appointment.html', context)


@login_required
def payment_page(request):
    """Step 2: Payment page"""
    appointment_id = request.session.get('appointment_id')
    if not appointment_id:
        messages.error(request, 'No appointment found. Please book an appointment first.')
        return redirect('home:home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            
            # Update appointment with payment method
            appointment.payment_method = payment_method
            appointment.save()
            
            # Redirect to payment processing
            return redirect('appointment:payment_process')
    else:
        form = PaymentMethodForm()
    
    context = {
        'appointment': appointment,
        'form': form,
    }
    return render(request, 'appointment/payment.html', context)

@login_required
def payment_process(request):
    """Step 3: Process payment"""
    appointment_id = request.session.get('appointment_id')
    if not appointment_id:
        messages.error(request, 'No appointment found.')
        return redirect('home:home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    
    # Check if payment transaction already exists
    if PaymentTransaction.objects.filter(appointment=appointment).exists():
        messages.info(request, 'Payment already processed for this appointment.')
        return redirect('appointment:confirmation', appointment_id=appointment.id)
    
    # Create payment transaction with unique transaction_id
    transaction = PaymentTransaction.objects.create(
        appointment=appointment,
        transaction_id=appointment.transaction_id or f"TXN-{uuid.uuid4().hex[:12].upper()}",
        amount=appointment.total_amount,
        method=appointment.payment_method or 'bkash',
        status='paid'
    )
    
    # Update appointment with transaction_id if empty
    if not appointment.transaction_id:
        appointment.transaction_id = transaction.transaction_id
        appointment.payment_status = 'paid'
        appointment.status = 'confirmed'
        appointment.save()
    
    # Clear session
    if 'appointment_id' in request.session:
        del request.session['appointment_id']
    
    messages.success(request, 'Payment successful! Your appointment is confirmed.')
    return redirect('appointment:confirmation', appointment_id=appointment.id)


@login_required
def appointment_confirmation(request, appointment_id):
    """Step 4: Confirmation page"""
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    
    context = {
        'appointment': appointment,
    }
    return render(request, 'appointment/confirmation.html', context)


@login_required
def appointment_list(request):
    """View all appointments for the user"""
    appointments = Appointment.objects.filter(patient=request.user).order_by('-created_at')
    
    context = {
        'appointments': appointments,
    }
    return render(request, 'appointment/list.html', context)


def calculate_fees(request):
    """AJAX endpoint to calculate fees"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            consultation_fee = Decimal(request.POST.get('consultation_fee', '0'))
            vat_amount = consultation_fee * Decimal('0.05')
            platform_fee = Decimal('29.00')
            total_amount = consultation_fee + vat_amount + platform_fee
            
            return JsonResponse({
                'success': True,
                'consultation_fee': float(consultation_fee),
                'vat_amount': float(vat_amount),
                'platform_fee': float(platform_fee),
                'total_amount': float(total_amount),
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})