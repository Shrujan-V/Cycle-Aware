from django import forms
from .models import CycleTracker

class CycleTrackerForm(forms.ModelForm):
    class Meta:
        model = CycleTracker
        fields = ['cycle_length', 'last_period_date', 'cramps', 'mood', 'did_train', 'performance_rating']
        widgets = {
            'last_period_date': forms.DateInput(attrs={'type': 'date'}),
            'performance_rating': forms.NumberInput(attrs={'min': '1', 'max': '5'}),
        }
from django import forms
from .models import Athlete

class AthleteTrackerForm(forms.ModelForm):
    class Meta:
        model = Athlete
        fields = ['durata', 'distot', 'hsr', 'acc', 'dec', 'rpe', 'srpe']
