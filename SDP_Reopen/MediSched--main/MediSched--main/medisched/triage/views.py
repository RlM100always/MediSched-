# triage/views.py - UPDATED VERSION
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages  # ADD THIS IMPORT
from django.core.exceptions import ObjectDoesNotExist

from .models import PatientSymptomLog, SymptomRule
from core.models import Symptom, Department
from doctor.models import Doctor
import json

# ==============================
# STRATEGY PATTERN IMPLEMENTATION
# ==============================

class SymptomAnalysisStrategy:
    """Base strategy class - Strategy Pattern"""
    def analyze(self, symptoms_input, selected_symptoms_ids):
        raise NotImplementedError("Subclasses must implement analyze method")


class RuleBasedAnalysis(SymptomAnalysisStrategy):
    """Rule-based analysis strategy"""
    def analyze(self, symptoms_input, selected_symptoms_ids):
        results = {
            'possible_conditions': [],
            'recommended_departments': [],
            'urgency_level': 'self_care',
            'urgency_score': 0,
            'advice': 'Monitor your symptoms. If they worsen, consult a doctor.',
            'red_flags': [],
            'confidence_score': 0.7
        }
        
        # Get selected symptoms
        selected_symptoms = Symptom.objects.filter(id__in=selected_symptoms_ids)
        
        if not selected_symptoms.exists() and not symptoms_input.strip():
            # No symptoms selected or described
            results['advice'] = 'Please describe your symptoms or select from the list for better analysis.'
            return results
        
        total_urgency = 0
        all_departments = set()
        all_conditions = set()
        symptom_count = 0
        
        for symptom in selected_symptoms:
            try:
                rule = SymptomRule.objects.get(symptom=symptom)
                total_urgency += rule.urgency_score
                symptom_count += 1
                
                # Add departments
                for dept in rule.related_departments.all():
                    all_departments.add(dept.id)
                
                # Add conditions
                for condition in rule.common_conditions:
                    all_conditions.add(condition)
                
                # Check red flags
                if rule.red_flags:
                    results['red_flags'].append(f"{symptom.name}: {rule.red_flags}")
                    
            except SymptomRule.DoesNotExist:
                # Default rule if not found
                total_urgency += 3
                symptom_count += 1
                results['possible_conditions'].append(f"Condition related to {symptom.name}")
        
        # Text analysis
        symptoms_lower = symptoms_input.lower()
        text_based_urgency = 0
        
        urgent_keywords = ['severe', 'emergency', 'cannot breathe', 'chest pain', 'unconscious']
        moderate_keywords = ['pain', 'fever', 'headache', 'cough', 'vomit']
        
        for keyword in urgent_keywords:
            if keyword in symptoms_lower:
                text_based_urgency = max(text_based_urgency, 8)
                
        for keyword in moderate_keywords:
            if keyword in symptoms_lower:
                text_based_urgency = max(text_based_urgency, 5)
        
        # Calculate average urgency
        if symptom_count > 0:
            avg_urgency = total_urgency / symptom_count
        else:
            avg_urgency = text_based_urgency if text_based_urgency > 0 else 3
        
        # Use the higher of calculated or text-based urgency
        final_urgency = max(avg_urgency, text_based_urgency)
        
        # Determine urgency level
        if final_urgency >= 8:
            results['urgency_level'] = 'emergency'
            results['advice'] = '⚠️ SEEK IMMEDIATE MEDICAL ATTENTION! Go to emergency department.'
            results['confidence_score'] = 0.9
        elif final_urgency >= 6:
            results['urgency_level'] = 'urgent'
            results['advice'] = 'Schedule an appointment within 24 hours.'
            results['confidence_score'] = 0.8
        elif final_urgency >= 4:
            results['urgency_level'] = 'routine'
            results['advice'] = 'Schedule a routine appointment.'
            results['confidence_score'] = 0.75
        else:
            results['urgency_level'] = 'self_care'
            results['advice'] = 'Monitor symptoms at home.'
            results['confidence_score'] = 0.7
        
        # Convert sets to lists
        results['recommended_departments'] = list(all_departments)
        
        if all_conditions:
            results['possible_conditions'] = list(all_conditions)
        elif not results['possible_conditions'] and symptoms_input:
            if 'fever' in symptoms_lower:
                results['possible_conditions'] = ['Viral infection', 'Common cold', 'Flu']
            elif 'headache' in symptoms_lower:
                results['possible_conditions'] = ['Tension headache', 'Migraine', 'Sinusitis']
            elif 'cough' in symptoms_lower:
                results['possible_conditions'] = ['Common cold', 'Bronchitis', 'Allergy']
            else:
                results['possible_conditions'] = ['General medical condition']
        
        results['urgency_score'] = final_urgency
        
        return results


# ==============================
# FACTORY PATTERN IMPLEMENTATION
# ==============================

class SymptomCheckerFactory:
    """Factory Pattern for creating analysis strategies"""
    @staticmethod
    def get_analyzer(analysis_type='rule_based'):
        return RuleBasedAnalysis()


# ==============================
# MAIN VIEWS
# ==============================

class SymptomCheckerView(LoginRequiredMixin, TemplateView):
    """Main symptom checker page"""
    template_name = 'triage/symptom_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['symptoms'] = Symptom.objects.all().order_by('name')
        return context


class AnalyzeSymptomsView(LoginRequiredMixin, View):
    """Analyze symptoms and show results"""
    
    def post(self, request):
        try:
            # Get form data
            symptoms_text = request.POST.get('symptoms_text', '').strip()
            selected_symptoms = request.POST.getlist('selected_symptoms', [])
            
            # Convert selected_symptoms to integers
            selected_symptoms_ids = []
            for symptom_id in selected_symptoms:
                try:
                    selected_symptoms_ids.append(int(symptom_id))
                except ValueError:
                    continue
            
            # FACTORY PATTERN: Get the analyzer
            factory = SymptomCheckerFactory()
            analyzer = factory.get_analyzer('rule_based')
            
            # STRATEGY PATTERN: Use the analyzer
            analysis_results = analyzer.analyze(symptoms_text, selected_symptoms_ids)
            
            # Get recommended departments
            department_ids = analysis_results.get('recommended_departments', [])
            recommended_departments = Department.objects.filter(id__in=department_ids)
            
            # Get REAL doctors from database
            recommended_doctors = []
            if department_ids:
                # Get doctors specialized in these departments
                recommended_doctors = Doctor.objects.filter(
                    departments__id__in=department_ids,
                    is_verified=True
                ).distinct()[:6]
            
            # If no doctors found by department, get top-rated doctors
            if not recommended_doctors:
                recommended_doctors = Doctor.objects.filter(
                    is_verified=True
                ).order_by('-rating', '-total_experience')[:4]
            
            # Get selected symptom objects
            selected_symptom_objects = []
            if selected_symptoms_ids:
                selected_symptom_objects = Symptom.objects.filter(id__in=selected_symptoms_ids)
            
            # Save to log
            symptom_log = PatientSymptomLog.objects.create(
                user=request.user,
                symptoms_input=symptoms_text if symptoms_text else "No description provided",
                urgency_level=analysis_results['urgency_level'],
                advice=analysis_results['advice'],
                possible_conditions=analysis_results['possible_conditions'],
                confidence_score=analysis_results.get('confidence_score', 0.7)
            )
            
            # Add many-to-many relationships
            if selected_symptoms_ids:
                symptom_log.selected_symptoms.set(selected_symptoms_ids)
            
            if department_ids:
                symptom_log.recommended_departments.set(department_ids)
            
            if recommended_doctors:
                symptom_log.recommended_doctors.set(recommended_doctors)
            
            # OBSERVER PATTERN: Notify other services
            print(f"OBSERVER: New symptom check logged for user {request.user.username}")
            print(f"OBSERVER: Urgency level: {analysis_results['urgency_level']}")
            print(f"OBSERVER: Selected symptoms: {len(selected_symptoms_ids)}")
            print(f"OBSERVER: Recommended doctors: {len(recommended_doctors)}")
            
            # Render results
            context = {
                'symptom_log': symptom_log,
                'recommended_doctors': recommended_doctors,
                'red_flags': analysis_results.get('red_flags', []),
                'selected_symptoms': selected_symptom_objects,
                'recommended_departments': recommended_departments,
                'urgency_score': analysis_results.get('urgency_score', 0),
            }
            
            return render(request, 'triage/results.html', context)
            
        except Exception as e:
            print(f"Error in symptom analysis: {str(e)}")
            # Use messages framework properly
            messages.error(request, "Please describe your symptoms or select symptoms from the list.")
            return redirect('triage:symptom_check')


class CreateAppointmentFromTriageView(LoginRequiredMixin, View):
    """Create appointment from triage results"""
    
    def post(self, request, log_id):
        try:
            symptom_log = get_object_or_404(PatientSymptomLog, id=log_id, user=request.user)
            doctor_id = request.POST.get('doctor_id')
            
            if not doctor_id:
                # If no doctor selected, redirect to appointment booking with triage data
                request.session['triage_data'] = {
                    'log_id': log_id,
                    'symptoms': symptom_log.symptoms_input,
                    'selected_symptoms': list(symptom_log.selected_symptoms.values_list('id', flat=True)),
                    'urgency': symptom_log.urgency_level,
                }
                return redirect('appointment:book_appointment')
            
            doctor = get_object_or_404(Doctor, id=doctor_id, is_verified=True)
            
            # Store data in session for appointment app to use
            request.session['triage_data'] = {
                'log_id': log_id,
                'doctor_id': doctor_id,
                'symptoms': symptom_log.symptoms_input,
                'selected_symptoms': list(symptom_log.selected_symptoms.values_list('id', flat=True)),
                'urgency': symptom_log.urgency_level,
            }
            
            # Mark as appointment created
            symptom_log.appointment_created = True
            symptom_log.save()
            
            return redirect('appointment:book_appointment')
            
        except Exception as e:
            print(f"Error creating appointment: {e}")
            messages.error(request, "Error creating appointment. Please try again.")
            return redirect('triage:symptom_check')


# ==============================
# API VIEWS
# ==============================

@method_decorator(csrf_exempt, name='dispatch')
class GetSymptomDetailsAPI(View):
    """API to get symptom details"""
    
    def get(self, request):
        try:
            symptom_id = request.GET.get('symptom_id')
            
            if not symptom_id:
                return JsonResponse({'error': 'No symptom ID provided'}, status=400)
            
            symptom = get_object_or_404(Symptom, id=symptom_id)
            
            try:
                rule = SymptomRule.objects.get(symptom=symptom)
                data = {
                    'success': True,
                    'symptom': {
                        'name': symptom.name,
                        'id': symptom.id
                    },
                    'related_departments': [
                        {'id': dept.id, 'name': dept.name} 
                        for dept in rule.related_departments.all()
                    ],
                    'urgency_score': rule.urgency_score,
                    'common_conditions': rule.common_conditions,
                    'red_flags': rule.red_flags,
                    'self_care_tips': rule.self_care_tips,
                }
            except SymptomRule.DoesNotExist:
                data = {
                    'success': True,
                    'symptom': {
                        'name': symptom.name,
                        'id': symptom.id
                    },
                    'related_departments': [],
                    'urgency_score': 3,
                    'common_conditions': [f"Condition related to {symptom.name}"],
                    'red_flags': 'No specific red flags defined',
                    'self_care_tips': 'Rest and monitor symptoms.',
                }
            
            return JsonResponse(data)
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class QuickTriageAPI(View):
    """Quick triage API for homepage"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            symptom_ids = data.get('symptoms', [])
            
            if not symptom_ids:
                return JsonResponse({'error': 'No symptoms provided'}, status=400)
            
            # Use factory and strategy patterns
            factory = SymptomCheckerFactory()
            analyzer = factory.get_analyzer('rule_based')
            results = analyzer.analyze('', symptom_ids)
            
            return JsonResponse(results)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
# Add this at the end of triage/views.py (after other views)

class SymptomHistoryView(LoginRequiredMixin, ListView):
    """View symptom check history"""
    model = PatientSymptomLog
    template_name = 'triage/history.html'
    context_object_name = 'symptom_logs'
    paginate_by = 10
    
    def get_queryset(self):
        return PatientSymptomLog.objects.filter(user=self.request.user).order_by('-created_at')
# Add this to triage/views.py (somewhere after other views)

class SymptomHistoryView(LoginRequiredMixin, ListView):
    """View symptom check history"""
    model = PatientSymptomLog
    template_name = 'triage/history.html'
    context_object_name = 'symptom_logs'
    paginate_by = 10
    
    def get_queryset(self):
        return PatientSymptomLog.objects.filter(user=self.request.user).order_by('-created_at')