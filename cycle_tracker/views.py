"""
views.py

Defines views for the Cycle Tracker application, including:
- Cycle tracking form handling.
- Athlete tracking and phase prediction using ML model.
- Prediction via API and storing results.
- Custom login handling.
- History view for tracking entries.
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import CycleTrackerForm, AthleteTrackerForm
from .models import CycleTracker, Athlete
from .ml_model import predict_phase

import json
import numpy as np

# -----------------------------
# Phase messages for UI feedback
# -----------------------------
PHASE_MESSAGES = {
    1: ("Menstrual", "Every champion knows that recovery is part of the process.\nTrust your body, honor the rest, and come back fiercer!"),
    2: ("Follicular", "You are limitless! Fresh energy, fresh focus—channel it into every move you make!"),
    3: ("Ovulation", "This is your moment—your strength, speed, and power are at their peak. Own it!"),
    4: ("Luteal", "Tough days build tougher athletes. Focus, breathe, and push through—you’ve got this!")
}

# -----------------------------
# Cycle Tracking View
# -----------------------------
def track_cycle(request):
    """
    Handles menstrual cycle tracking form submissions.
    Saves cycle data and displays next predicted period date.
    """
    if request.method == 'POST':
        form = CycleTrackerForm(request.POST)
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
        form = CycleTrackerForm()
    
    return render(request, 'cycle_tracker/track_form.html', {'form': form})

# -----------------------------
# Custom Login View
# -----------------------------
def custom_login(request):
    """
    Handles custom login for the Cycle Tracker app.
    Uses a hardcoded user for demonstration; replace with proper authentication.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username == "Shreya" and password == "Shreya":
            return redirect('cycle_tracker:track')
        else:
            return render(request, 'cycle_tracker/login.html', {
                'error_message': 'Invalid username or password.',
            })
    else:
        return render(request, 'cycle_tracker/login.html')

# -----------------------------
# History View
# -----------------------------
class HistoryView(ListView):
    """
    Displays a history of cycle tracking entries for the user, ordered by date.
    """
    model = CycleTracker
    template_name = 'cycle_tracker/history.html'
    context_object_name = 'entries'
    ordering = ['-tracking_date']

# -----------------------------
# Athlete Tracking View
# -----------------------------
def track_athlete(request):
    """
    Handles athlete training data input, predicts menstrual phase using ML,
    and displays the phase name and motivational message.
    """
    if request.method == 'POST':
        form = AthleteTrackerForm(request.POST)
        if form.is_valid():
            athlete = form.save(commit=False)
            features = [
                athlete.durata, athlete.distot, athlete.hsr,
                athlete.acc, athlete.dec, athlete.rpe, athlete.srpe
            ]
            athlete.phase_prediction = int(predict_phase(features))
            athlete.save()

            phase_name, phase_message = PHASE_MESSAGES.get(
                athlete.phase_prediction, ("Unknown", "No message available.")
            )

            return render(request, 'cycle_tracker/prediction_result.html', {
                'athlete': athlete,
                'phase_prediction': athlete.phase_prediction,
                'phase_name': phase_name,
                'phase_message': phase_message
            })
    else:
        form = AthleteTrackerForm()

    return render(request, 'cycle_tracker/track_athlete.html', {'form': form})

# -----------------------------
# JSON Encoder for NumPy types
# -----------------------------
class NpEncoder(json.JSONEncoder):
    """
    JSON encoder to handle NumPy data types for API responses.
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

# -----------------------------
# Predict and Store via API
# -----------------------------
def predict_and_store(request):
    """
    Handles JSON or form POST requests to predict phase and store athlete data.
    Returns an HTML page with prediction results or error page if failed.
    """
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST.dict()

            # Convert potential NumPy types
            cleaned_data = {
                key: int(value) if isinstance(value, np.integer) else value
                for key, value in data.items()
            }

            athlete = Athlete.objects.create(**cleaned_data)

            return render(request, 'cycle_tracker/prediction_result.html', {
                'athlete': athlete,
                'phase_prediction': athlete.phase_prediction
            })

        except Exception as e:
            return render(request, 'cycle_tracker/error.html', {'error_message': str(e)})
