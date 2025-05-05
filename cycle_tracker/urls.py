from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView  # Add this import

app_name = 'cycle_tracker'

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView  # Import only LogoutView if using custom login

app_name = 'cycle_tracker'

urlpatterns = [
    path('track/', views.track_cycle, name='track'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('athlete/', views.track_athlete, name='athletes'),
    path('predict/', views.predict_and_store, name='predict_and_store'),
    path('login/', views.custom_login, name='login'),  # Use custom_login view
    path('logout/', LogoutView.as_view(next_page='cycle_tracker:login'), name='logout'),
]

