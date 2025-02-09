from django.db import models
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from .ml_model import predict_phase 

class Athlete(models.Model):
    tracking_date = models.DateField(auto_now_add=True)
    durata = models.FloatField(help_text="Duration in minutes")
    distot = models.FloatField(help_text="Total distance in meters")
    hsr = models.FloatField(help_text="High-speed running distance in meters")
    acc = models.IntegerField(help_text="Number of accelerations")
    dec = models.IntegerField(help_text="Number of decelerations")
    rpe = models.IntegerField(help_text="Rating of Perceived Exertion (1-10)")
    srpe = models.FloatField(help_text="Session RPE")
    phase_prediction = models.IntegerField(default=0)  

    def save(self, *args, **kwargs):
        """
        Overrides save method to predict phase before saving.
        """
        input_data = [self.durata, self.distot, self.hsr, self.acc, self.dec, self.rpe, self.srpe]
        self.phase_prediction = predict_phase(input_data)  # Call ML model
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Athlete - {self.tracking_date} - Phase: {self.phase_prediction}"
    

    def calculate_next_period(self):
        return self.last_period_date + timedelta(days=self.cycle_length)

    def __str__(self):
        return f"{self.athlete.name if self.athlete else 'Unknown Athlete'} - {self.tracking_date}"


class CycleTracker(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='cycles', null=True, blank=True)
    cycle_length = models.PositiveIntegerField(help_text="Length of menstrual cycle in days")
    last_period_date = models.DateField()
    tracking_date = models.DateField(auto_now_add=True)
    cramps = models.CharField(max_length=10, choices=[
        ('none', 'None'), ('mild', 'Mild'), ('moderate', 'Moderate'), ('severe', 'Severe')
    ])
    mood = models.CharField(max_length=10, choices=[
        ('happy', 'Happy'), ('neutral', 'Neutral'), ('irritable', 'Irritable'),
        ('anxious', 'Anxious'), ('sad', 'Sad')
    ])
    did_train = models.BooleanField(default=False)
    performance_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True
    )

    def calculate_next_period(self):
        return self.last_period_date + timedelta(days=self.cycle_length)

    def __str__(self):
        return f"{self.athlete.name if self.athlete else 'Unknown Athlete'} - {self.tracking_date}"
