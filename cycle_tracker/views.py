from django.shortcuts import render, redirect
from django.views.generic import ListView
from .forms import CycleTrackerForm
from .models import CycleTracker, Athlete  # Ensure Athlete model exists
from datetime import datetime

def track_cycle(request):
    if request.method == 'POST':
        form = CycleTrackerForm(request.POST)
        print("Form Data:", request.POST)  # Debugging

        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['did_train'] = 'did_train' in request.POST

            if not cleaned_data.get('performance_rating'):
                cleaned_data['performance_rating'] = None

            tracker = CycleTracker(**cleaned_data)
            tracker.save()

            next_period = tracker.calculate_next_period()
            return render(request, 'cycle_tracker/success.html', {'next_period': next_period})
        else:
            print("Form Errors:", form.errors)  # Debugging
    else:
        form = CycleTrackerForm()
    
    return render(request, 'cycle_tracker/track_form.html', {'form': form})


class HistoryView(ListView):
    model = CycleTracker
    template_name = 'cycle_tracker/history.html'
    context_object_name = 'entries'
    ordering = ['-tracking_date']


from django.shortcuts import render, redirect
from .forms import AthleteTrackerForm
from .models import Athlete

def track_athlete(request):
    if request.method == 'POST':
        form = AthleteTrackerForm(request.POST)
        if form.is_valid():
            form.save()
            
    else:
        form = AthleteTrackerForm()
    
    return render(request, 'cycle_tracker/track_athlete.html', {'form': form})
