"""
apps.py

Configuration for the Cycle Tracker Django application.
"""

from django.apps import AppConfig

class CycleTrackerConfig(AppConfig):
    """
    AppConfig for the cycle_tracker app.

    Attributes:
        default_auto_field (str): Specifies the type of primary key to use for models.
        name (str): The name of the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cycle_tracker'
