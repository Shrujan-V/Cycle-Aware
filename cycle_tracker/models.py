"""
models.py

Defines Django models for the Cycle Tracker application, including:

- Athlete: Tracks daily athlete training metrics and predicts menstrual phase using the ML model.
- CycleTracker: Tracks menstrual cycle details linked to athletes, used for phase-aware performance analysis.
"""

from django.db import models
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from .ml_model import predict_phase

class Athlete(models.Model):
    """
    Model to store athlete training metrics and predicted menstrual phase.

    Fields:
        tracking_date (Date): Auto-filled with the date of entry.
        durata (Float): Duration of training in minutes.
        distot (Float): Total distance covered in meters.
        hsr (Float): High-speed running distance in meters.
        acc (Integer): Number of accelerations.
        dec (Integer): Number of decelerations.
        rpe (Integer): Rating of Perceived Exertion (1-10).
        srpe (Float): Session RPE (rpe * duration).
        phase_prediction (Integer): Predicted menstrual phase label from the ML model.
    """

    tracking_date = models.DateField(auto_now_add=True)
    durata = models.FloatField(help_text="Duration in minutes")
    distot = models.FloatField(help_text="Total distance in meters")
    hsr = models.FloatField(help_text="High-speed running distance in meters")
    acc = models.IntegerField(help_text="Number of accelerations")
    dec = models.IntegerField(help_text="Number of decelerations")
    rpe = models.IntegerField(help_text="Rating of Perceived Exertion (1-10)")
    srpe = models.FloatField(help_text="Session RPE")
    phase_prediction = models.IntegerField(default=0, help_text="Predicted phase label (0: follicular, 1: luteal, etc.)")

    def save(self, *args, **kwargs):
        """
        Overrides the save method to predict the menstrual phase using the
        trained ML model before saving the instance.
        """
        input_data = [self.durata, self.distot, self.hsr, self.acc, self.dec, self.rpe, self.srpe]
        self.phase_prediction = predict_phase(input_data)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the Athlete entry.
        """
        return f"Athlete - {self.tracking_date} - Phase: {self.phase_prediction}"

class CycleTracker(models.Model):
    """
    Model to track menstrual cycle details for an athlete.

    Fields:
        athlete (ForeignKey): Links the entry to an Athlete instance.
        cycle_length (PositiveInteger): Length of menstrual cycle in days.
        last_period_date (Date): Date of the last period.
        tracking_date (Date): Auto-filled with the date of entry.
        cramps (Char): Severity of cramps.
        mood (Char): Mood on the tracked day.
        did_train (Boolean): Whether the athlete trained on the day.
        performance_rating (PositiveInteger): Athlete's performance rating (1-5).
    """

    athlete = models.ForeignKey(
        Athlete,
        on_delete=models.CASCADE,
        related_name='cycles',
        null=True,
        blank=True,
        help_text="Associated athlete for this cycle entry"
    )
    cycle_length = models.PositiveIntegerField(help_text="Length of menstrual cycle in days")
    last_period_date = models.DateField(help_text="Date of the last menstrual period")
    tracking_date = models.DateField(auto_now_add=True, help_text="Date this entry was created")
    cramps = models.CharField(
        max_length=10,
        choices=[
            ('none', 'None'),
            ('mild', 'Mild'),
            ('moderate', 'Moderate'),
            ('severe', 'Severe')
        ],
        help_text="Severity of cramps"
    )
    mood = models.CharField(
        max_length=10,
        choices=[
            ('happy', 'Happy'),
            ('neutral', 'Neutral'),
            ('irritable', 'Irritable'),
            ('anxious', 'Anxious'),
            ('sad', 'Sad')
        ],
        help_text="Mood on the tracked day"
    )
    did_train = models.BooleanField(default=False, help_text="Did the athlete train on this day?")
    performance_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text="Athlete's performance rating (1-5)"
    )

    def calculate_next_period(self):
        """
        Calculates the estimated next period date based on the last period date and cycle length.

        Returns:
            datetime.date: The estimated next period date.
        """
        return self.last_period_date + timedelta(days=self.cycle_length)

    def __str__(self):
        """
        String representation of the CycleTracker entry.
        """
        athlete_name = getattr(self.athlete, 'name', 'Unknown Athlete')
        return f"{athlete_name} - {self.tracking_date}"
