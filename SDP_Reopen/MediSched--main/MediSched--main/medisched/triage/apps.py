# triage/apps.py
from django.apps import AppConfig


class TriageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'triage'

    def ready(self):
        import triage.templatetags.custom_filters
