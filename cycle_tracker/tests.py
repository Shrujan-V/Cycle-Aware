"""
tests.py

Contains unit tests for the Cycle Tracker application.
"""

from django.test import TestCase

# No tests implemented yet.
# You can add tests like:

# from .models import Athlete, CycleTracker
# from datetime import date

# class AthleteModelTest(TestCase):
#     def test_phase_prediction_on_save(self):
#         athlete = Athlete.objects.create(
#             durata=60,
#             distot=5000,
#             hsr=1200,
#             acc=10,
#             dec=8,
#             rpe=7,
#             srpe=420
#         )
#         self.assertIsInstance(athlete.phase_prediction, int)

# class CycleTrackerModelTest(TestCase):
#     def test_next_period_calculation(self):
#         athlete = Athlete.objects.create(
#             durata=60, distot=5000, hsr=1200, acc=10, dec=8, rpe=7, srpe=420
#         )
#         cycle = CycleTracker.objects.create(
#             athlete=athlete,
#             cycle_length=28,
#             last_period_date=date(2025, 6, 1),
#             cramps='mild',
#             mood='happy',
#             did_train=True,
#             performance_rating=4
#         )
#         expected_date = date(2025, 6, 29)
#         self.assertEqual(cycle.calculate_next_period(), expected_date)
