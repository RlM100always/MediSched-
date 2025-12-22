# populate_triage.py (run this once to create sample data)
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medisched.settings')
django.setup()

from core.models import Symptom, Department
from triage.models import SymptomRule

def create_sample_rules():
    print("Creating sample symptom rules...")
    
    # Get or create departments
    general_medicine, _ = Department.objects.get_or_create(name="General Medicine")
    cardiology, _ = Department.objects.get_or_create(name="Cardiology")
    dermatology, _ = Department.objects.get_or_create(name="Dermatology")
    gastroenterology, _ = Department.objects.get_or_create(name="Gastroenterology")
    neurology, _ = Department.objects.get_or_create(name="Neurology")
    
    # Create or update symptom rules
    symptoms_data = [
        {
            'name': 'Fever',
            'departments': [general_medicine],
            'urgency': 4,
            'conditions': ['Viral infection', 'Bacterial infection', 'Flu', 'Common cold'],
            'red_flags': 'Fever above 104°F (40°C), lasting more than 3 days, with stiff neck or confusion',
            'self_care': 'Rest, drink plenty of fluids, take paracetamol if needed'
        },
        {
            'name': 'Headache',
            'departments': [general_medicine, neurology],
            'urgency': 3,
            'conditions': ['Migraine', 'Tension headache', 'Sinusitis'],
            'red_flags': 'Sudden severe headache, headache after injury, with fever and stiff neck',
            'self_care': 'Rest in dark room, stay hydrated, avoid triggers'
        },
        {
            'name': 'Chest Pain',
            'departments': [cardiology, general_medicine],
            'urgency': 9,
            'conditions': ['Angina', 'Heart attack', 'Acid reflux', 'Muscle strain'],
            'red_flags': 'Chest pain spreading to arm/jaw, shortness of breath, dizziness',
            'self_care': 'Seek IMMEDIATE emergency care for chest pain'
        },
        {
            'name': 'Skin Rash',
            'departments': [dermatology, general_medicine],
            'urgency': 3,
            'conditions': ['Allergy', 'Eczema', 'Psoriasis', 'Fungal infection'],
            'red_flags': 'Rash with fever, difficulty breathing, spreading rapidly',
            'self_care': 'Avoid scratching, use mild soap, keep area clean and dry'
        },
        {
            'name': 'Stomach Pain',
            'departments': [gastroenterology, general_medicine],
            'urgency': 5,
            'conditions': ['Gastritis', 'Food poisoning', 'Appendicitis', 'Irritable bowel'],
            'red_flags': 'Severe pain, vomiting blood, black stools, high fever',
            'self_care': 'Clear liquids only, avoid spicy/fatty foods, rest'
        },
        {
            'name': 'Cough',
            'departments': [general_medicine],
            'urgency': 3,
            'conditions': ['Common cold', 'Bronchitis', 'Allergy', 'Asthma'],
            'red_flags': 'Coughing blood, difficulty breathing, chest pain with cough',
            'self_care': 'Drink warm liquids, use honey, avoid irritants'
        }
    ]
    
    for data in symptoms_data:
        symptom, created = Symptom.objects.get_or_create(name=data['name'])
        
        rule, rule_created = SymptomRule.objects.update_or_create(
            symptom=symptom,
            defaults={
                'urgency_score': data['urgency'],
                'common_conditions': data['conditions'],
                'red_flags': data['red_flags'],
                'self_care_tips': data['self_care']
            }
        )
        
        # Clear and add departments
        rule.related_departments.clear()
        for dept in data['departments']:
            rule.related_departments.add(dept)
        
        print(f"{'Created' if rule_created else 'Updated'} rule for {data['name']}")
    
    print("Sample symptom rules created successfully!")

if __name__ == '__main__':
    create_sample_rules()