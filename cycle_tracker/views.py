from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import ListView
from .forms import CycleTrackerForm, AthleteTrackerForm
from .models import CycleTracker, Athlete
from .ml_model import predict_phase  # Import ML function
import json
import numpy as np
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Cycle Tracking View

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


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

# Define a custom login view (if you want to avoid using Django's default LoginView)
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        
        if username=="Shreya" and password=="Shreya":
            # Log the user in
            return redirect('cycle_tracker:track')  # Redirect to a page after login (e.g., home or track)
        else:
            # Invalid login credentials
            return render(request, 'cycle_tracker/login.html', {
                'error_message': 'Invalid username or password.',
            })
    else:
        return render(request, 'cycle_tracker/login.html')


class HistoryView(ListView):
    model = CycleTracker
    template_name = 'cycle_tracker/history.html'
    context_object_name = 'entries'
    ordering = ['-tracking_date']


# Athlete Tracking View
from django.shortcuts import render
from .forms import AthleteTrackerForm
from .models import Athlete
from .ml_model import predict_phase  # Import ML function

from django.shortcuts import render
from .forms import AthleteTrackerForm
from .models import Athlete
from .ml_model import predict_phase  # Import ML function

# Define phase names and messages
PHASE_MESSAGES = {
    1: ("Menstrual", "Every champion knows that recovery is part of the process.\nTrust your body, honor the rest, and come back fiercer!"),
    2: ("Follicular", "You are limitless! Fresh energy, fresh focus—channel it into every move you make!"),
    3: ("Ovulation", "This is your moment—your strength, speed, and power are at their peak. Own it!"),
    4: ("Luteal", "Tough days build tougher athletes. Focus, breathe, and push through—you’ve got this!")
}


def track_athlete(request):
    if request.method == 'POST':
        form = AthleteTrackerForm(request.POST)
        if form.is_valid():
            athlete = form.save(commit=False)

            # Prepare feature list for ML model
            features = [
                athlete.durata, athlete.distot, athlete.hsr,
                athlete.acc, athlete.dec, athlete.rpe, athlete.srpe
            ]
            athlete.phase_prediction = int(predict_phase(features))  # ML Prediction
            athlete.save()

            # Get the phase name and message
            phase_name, phase_message = PHASE_MESSAGES.get(athlete.phase_prediction, ("Unknown", "No message available."))

            # Render the result in an HTML page
            return render(request, 'cycle_tracker/prediction_result.html', {
                'athlete': athlete,
                'phase_prediction': athlete.phase_prediction,
                'phase_name': phase_name,
                'phase_message': phase_message
            })

    else:
        form = AthleteTrackerForm()

    return render(request, 'cycle_tracker/track_athlete.html', {'form': form})



from django.shortcuts import render
import json
import numpy as np
from django.http import JsonResponse
from .models import Athlete
from .ml_model import predict_phase  # Ensure ML function is imported

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def predict_and_store(request):
    if request.method == 'POST':
        try:
            # Check if request has JSON data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST.dict()  # Convert form data to dictionary

            # Convert NumPy types to Python native types
            cleaned_data = {key: int(value) if isinstance(value, np.integer) else value for key, value in data.items()}

            # Save the athlete entry
            athlete = Athlete.objects.create(**cleaned_data)

            return render(request, 'cycle_tracker/prediction_result.html', {
                'athlete': athlete,
                'phase_prediction': athlete.phase_prediction
            })

        except Exception as e:
            return render(request, 'cycle_tracker/error.html', {'error_message': str(e)})
