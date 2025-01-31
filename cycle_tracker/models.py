from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta

class CycleTracker(models.Model):
    CRAMP_CHOICES = [
        ('none', 'None'),
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ]
    
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('neutral', 'Neutral'),
        ('irritable', 'Irritable'),
        ('anxious', 'Anxious'),
        ('sad', 'Sad'),
    ]
    
    # Cycle Information
    cycle_length = models.PositiveIntegerField(
        #validators=[MinValueValidator(1), MaxValueValidator()],
        help_text="Length of menstrual cycle in days"
    )
    last_period_date = models.DateField()
    
    # Daily Tracking
    tracking_date = models.DateField(auto_now_add=True)
    cramps = models.CharField(max_length=10, choices=CRAMP_CHOICES)
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES)
    
    # Training Information
    did_train = models.BooleanField(default=False)
    performance_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    
    def calculate_next_period(self):
        return self.last_period_date + timedelta(days=self.cycle_length)
    
    def __str__(self):
        return f"Cycle Track - {self.tracking_date}"