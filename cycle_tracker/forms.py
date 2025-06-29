"""
forms.py

Contains Django ModelForm classes for handling form data input for
CycleTracker and Athlete models within the Cycle Tracker application.
"""

from django import forms
from .models import CycleTracker, Athlete

class CycleTrackerForm(forms.ModelForm):
    """
    Form for tracking cycle-related details for the CycleTracker model.

    Fields:
        - cycle_length (int): Length of the menstrual cycle in days.
        - last_period_date (date): Date of the last menstrual period.
        - cramps (bool): Whether cramps were experienced.
        - mood (str): Mood description.
        - did_train (bool): Whether the athlete trained on the given day.
        - performance_rating (int): Athlete's self-rated performance (1-5).

    Widgets:
        - last_period_date: Uses a date picker in the frontend.
        - performance_rating: Uses a number input with min=1 and max=5.
    """
    class Meta:
        model = CycleTracker
        fields = ['cycle_length', 'last_period_date', 'cramps', 'mood', 'did_train', 'performance_rating']
        widgets = {
            'last_period_date': forms.DateInput(attrs={'type': 'date'}),
            'performance_rating': forms.NumberInput(attrs={'min': '1', 'max': '5'}),
        }

class AthleteTrackerForm(forms.ModelForm):
    """
    Form for tracking athlete training metrics for the Athlete model.

    Fields:
        - durata (float): Duration of training session.
        - distot (float): Total distance covered.
        - hsr (float): High-speed running distance.
        - acc (int): Number of accelerations.
        - dec (int): Number of decelerations.
        - rpe (int): Rate of perceived exertion.
        - srpe (float): Session RPE (computed as rpe * duration).
    """
    class Meta:
        model = Athlete
        fields = ['durata', 'distot', 'hsr', 'acc', 'dec', 'rpe', 'srpe']
