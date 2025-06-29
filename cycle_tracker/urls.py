"""
urls.py

Defines URL patterns for the Cycle Tracker application, mapping routes to views
for cycle tracking, athlete data management, prediction, and authentication.
"""

from django.urls import path
from django.contrib.auth.views import LogoutView  # Import only LogoutView if using custom login
from . import views

app_name = 'cycle_tracker'

urlpatterns = [
    path('track/', views.track_cycle, name='track'),
    # Displays user's cycle tracking history
    path('history/', views.HistoryView.as_view(), name='history'),
    # Form to input athlete training data and view predictions
    path('athlete/', views.track_athlete, name='athletes'),
    # Endpoint to predict menstrual phase and store the result
    path('predict/', views.predict_and_store, name='predict_and_store'),
    # Custom login view for user authentication
    path('login/', views.custom_login, name='login'),
    # Uses Django's built-in LogoutView with redirection to login after logout
    path('logout/', LogoutView.as_view(next_page='cycle_tracker:login'), name='logout'),
]
