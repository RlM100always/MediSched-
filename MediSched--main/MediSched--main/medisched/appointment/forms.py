from django import forms
from .models import Appointment
import re

class AppointmentForm(forms.ModelForm):
    patient_phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '01XXXXXXXXX',
            'class': 'form-control',
            'pattern': '^(?:\+?88)?01[3-9]\d{8}$'
        })
    )
    
    consultation_type = forms.ChoiceField(
        choices=[('general', 'General Consultation'), ('special', 'Special Consultation')],
        widget=forms.RadioSelect()
    )
    
    appointment_type = forms.ChoiceField(
        choices=[('instant', 'Instant Video Consultation'), ('scheduled', 'Book an Appointment')],
        widget=forms.RadioSelect()
    )
    
    class Meta:
        model = Appointment
        fields = ['patient_phone', 'consultation_type', 'appointment_type', 'patient_name', 'patient_age', 'patient_gender', 'symptoms']
    
    def clean_patient_phone(self):
        phone = self.cleaned_data.get('patient_phone')
        
        # Remove any spaces or dashes
        phone = re.sub(r'[\s\-]+', '', phone)
        
        # Bangladeshi phone number validation
        pattern = r'^(?:\+?88)?01[3-9]\d{8}$'
        
        if not re.match(pattern, phone):
            raise forms.ValidationError("Please enter a valid Bangladeshi phone number (e.g., 013XXXXXXXX or +88013XXXXXXXX)")
        
        # Ensure 11 digits (without +88)
        if phone.startswith('+88'):
            phone = '0' + phone[3:]
        elif phone.startswith('88'):
            phone = '0' + phone[2:]
        
        return phone


class PaymentMethodForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=[
            ('bkash', 'bKash'),
            ('nagad', 'Nagad'),
            ('card', 'Card'),
            ('mobile_banking', 'Mobile Banking'),
        ],
        widget=forms.RadioSelect()
    )