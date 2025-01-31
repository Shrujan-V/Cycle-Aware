from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .forms import CycleTrackerForm
from .models import CycleTracker
from datetime import datetime

def track_cycle(request):
    if request.method == 'POST':
        form = CycleTrackerForm(request.POST)
        print("Form Data:", request.POST)  # Debugging

        if form.is_valid():
            # Get the form data
            cleaned_data = form.cleaned_data
            # Handle checkbox for did_train
            cleaned_data['did_train'] = True if 'did_train' in request.POST else False
            
            # Handle blank performance_rating
            if 'performance_rating' not in cleaned_data or cleaned_data['performance_rating'] == '':
                cleaned_data['performance_rating'] = None

            # Save the form with the cleaned data
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
