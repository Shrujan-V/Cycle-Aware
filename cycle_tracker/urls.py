from django.urls import path
from . import views

app_name = 'cycle_tracker'

urlpatterns = [
    path('track/', views.track_cycle, name='track'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('athlete/',views.track_athlete, name='athletes'),
]