from django import forms
from .models import Message, Prescription, TestReport, VideoCall
from django.utils import timezone

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'file', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Type your message here...',
                'class': 'form-control'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.txt'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['diagnosis', 'advice', 'follow_up_date', 'medicines', 'suggested_tests']
        widgets = {
            'diagnosis': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter diagnosis...',
                'class': 'form-control'
            }),
            'advice': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Medical advice for patient...',
                'class': 'form-control'
            }),
            'follow_up_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': timezone.now().date().isoformat()
            }),
            'medicines': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Enter medicines in JSON format or use the form below',
                'class': 'form-control'
            }),
            'suggested_tests': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter suggested tests in JSON format or use the form below',
                'class': 'form-control'
            }),
        }


class MedicineForm(forms.Form):
    """Form for adding individual medicine"""
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Medicine name'
    }))
    dosage = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'e.g., 1-0-1'
    }))
    duration = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'e.g., 7 days'
    }))
    instructions = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Special instructions'
    }))


class TestReportForm(forms.ModelForm):
    class Meta:
        model = TestReport
        fields = ['test_name', 'test_date', 'lab_name', 'report_file', 'findings']
        widgets = {
            'test_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., CBC, Blood Sugar, X-Ray'
            }),
            'test_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'lab_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Laboratory name'
            }),
            'report_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'findings': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Test findings/results...'
            }),
        }


class VideoCallForm(forms.ModelForm):
    class Meta:
        model = VideoCall
        fields = ['call_type', 'scheduled_time', 'notes']
        widgets = {
            'call_type': forms.Select(attrs={'class': 'form-control'}),
            'scheduled_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Any notes about the call...'
            }),
        }