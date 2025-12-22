# triage/ai_analyzer.py
import re
import json
from typing import List, Dict, Tuple
from datetime import datetime

class EnhancedSymptomAnalyzer:
    """DeepSeek-like symptom analyzer with better prompts"""
    
    def __init__(self):
        self.symptom_keywords = {
            'fever': {
                'severity_keywords': ['high fever', '104°F', '40°C', 'very high'],
                'duration_keywords': ['days', 'weeks', 'months'],
                'associated': ['headache', 'body ache', 'chills', 'sweating'],
                'urgency_score': 6,
                'conditions': ['Viral infection', 'Bacterial infection', 'Malaria', 'Dengue', 'Typhoid'],
                'departments': ['General Medicine', 'Infectious Diseases'],
                'red_flags': ['Fever >104°F', 'lasts >3 days', 'with stiff neck', 'with rash']
            },
            'headache': {
                'severity_keywords': ['severe', 'worst', 'throbbing', 'unbearable'],
                'duration_keywords': ['sudden', 'chronic', 'persistent'],
                'associated': ['nausea', 'vomiting', 'vision', 'light sensitivity'],
                'urgency_score': 5,
                'conditions': ['Migraine', 'Tension headache', 'Sinusitis', 'Cluster headache'],
                'departments': ['Neurology', 'General Medicine'],
                'red_flags': ['sudden severe', 'after injury', 'with fever', 'with confusion']
            },
            'chest pain': {
                'severity_keywords': ['sharp', 'crushing', 'pressure', 'tightness'],
                'duration_keywords': ['minutes', 'hours', 'radiating'],
                'associated': ['shortness of breath', 'sweating', 'dizziness', 'nausea'],
                'urgency_score': 9,  # HIGH urgency
                'conditions': ['Angina', 'Heart attack', 'Acid reflux', 'Pulmonary embolism'],
                'departments': ['Cardiology', 'Emergency Medicine'],
                'red_flags': ['radiates to arm/jaw', 'with sweating', 'with shortness of breath']
            },
            'cough': {
                'severity_keywords': ['persistent', 'severe', 'dry', 'productive'],
                'duration_keywords': ['weeks', 'chronic'],
                'associated': ['fever', 'phlegm', 'chest pain', 'wheezing'],
                'urgency_score': 4,
                'conditions': ['Bronchitis', 'Pneumonia', 'Asthma', 'Allergy', 'COVID-19'],
                'departments': ['Pulmonology', 'General Medicine'],
                'red_flags': ['coughing blood', 'difficulty breathing', 'high fever']
            }
        }
    
    def analyze_symptoms(self, symptoms_text: str, selected_symptoms: List[str]) -> Dict:
        """Analyze symptoms with enhanced logic"""
        
        symptoms_lower = symptoms_text.lower()
        
        # Extract keywords
        duration = self._extract_duration(symptoms_text)
        severity = self._detect_severity(symptoms_text)
        
        # Analyze each selected symptom
        results = {
            'possible_conditions': [],
            'recommended_departments': [],
            'urgency_score': 3,
            'advice': '',
            'analysis_method': 'enhanced_rule_based',
            'confidence_score': 0.85,
            'duration_detected': duration,
            'severity_detected': severity,
            'key_findings': []
        }
        
        # Process selected symptoms
        urgency_scores = []
        all_conditions = set()
        all_departments = set()
        
        for symptom_name in selected_symptoms:
            if symptom_name.lower() in self.symptom_keywords:
                symptom_info = self.symptom_keywords[symptom_name.lower()]
                
                # Adjust urgency based on severity keywords
                base_urgency = symptom_info['urgency_score']
                if severity == 'high':
                    base_urgency += 2
                elif severity == 'moderate':
                    base_urgency += 1
                
                # Check if duration keywords exist
                if duration:
                    base_urgency += 1
                
                urgency_scores.append(base_urgency)
                all_conditions.update(symptom_info['conditions'])
                all_departments.update(symptom_info['departments'])
                
                # Add key finding
                finding = f"{symptom_name.capitalize()} detected"
                if severity:
                    finding += f" ({severity} severity)"
                if duration:
                    finding += f" ({duration})"
                results['key_findings'].append(finding)
        
        # Calculate final urgency
        if urgency_scores:
            results['urgency_score'] = max(urgency_scores)
        else:
            # Text-based urgency
            if any(word in symptoms_lower for word in ['emergency', 'cannot breathe', 'unconscious']):
                results['urgency_score'] = 9
            elif any(word in symptoms_lower for word in ['severe', 'intense', 'worst']):
                results['urgency_score'] = 7
            elif any(word in symptoms_lower for word in ['moderate', 'persistent']):
                results['urgency_score'] = 5
        
        # Determine urgency level
        if results['urgency_score'] >= 8:
            results['urgency_level'] = 'emergency'
            results['advice'] = self._get_emergency_advice()
        elif results['urgency_score'] >= 6:
            results['urgency_level'] = 'urgent'
            results['advice'] = f"Your symptoms ({severity or 'moderate'} severity) require attention within 24 hours. Based on {duration or 'recent'} symptoms, consider: {', '.join(list(all_conditions)[:3])}"
        elif results['urgency_score'] >= 4:
            results['urgency_level'] = 'routine'
            results['advice'] = f"Schedule a consultation. Symptoms suggest possible {', '.join(list(all_conditions)[:2]) if all_conditions else 'medical condition'}. Monitor for changes."
        else:
            results['urgency_level'] = 'self_care'
            results['advice'] = "Monitor symptoms. Try self-care measures. If symptoms persist beyond 3 days, consult a doctor."
        
        # Add conditions and departments
        results['possible_conditions'] = list(all_conditions)[:5]  # Top 5 conditions
        results['recommended_departments'] = list(all_departments)
        
        # Add personalized note
        if duration:
            results['advice'] += f" Note: Symptoms reported for {duration}."
        
        return results
    
    def _extract_duration(self, text: str) -> str:
        """Extract duration from text"""
        patterns = [
            (r'for (\d+)\s*(day|days)', '{} day(s)'),
            (r'for (\d+)\s*(week|weeks)', '{} week(s)'),
            (r'for (\d+)\s*(month|months)', '{} month(s)'),
            (r'(\d+)\s*(day|days) ago', 'started {} day(s) ago'),
            (r'since (\w+ \d+)', 'since {}'),
        ]
        
        for pattern, template in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return template.format(*match.groups())
        
        return ''
    
    def _detect_severity(self, text: str) -> str:
        """Detect symptom severity"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['severe', 'extreme', 'unbearable', 'worst', 'intense']):
            return 'high'
        elif any(word in text_lower for word in ['moderate', 'persistent', 'ongoing', 'constant']):
            return 'moderate'
        elif any(word in text_lower for word in ['mild', 'slight', 'minor']):
            return 'low'
        
        return ''
    
    def _get_emergency_advice(self) -> str:
        return """🚨 EMERGENCY - SEEK IMMEDIATE MEDICAL ATTENTION!
        
Based on your symptoms, you should:
1. Go to the nearest emergency department IMMEDIATELY
2. Call emergency services (999 in Bangladesh)
3. Do not wait or self-medicate
4. Inform someone about your condition

Symptoms like chest pain, difficulty breathing, or severe symptoms require urgent evaluation."""