import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')
django.setup()

from workoutplans.utils import generate_workout_plan

test_input = """
Age: 30
Fitness Level: Intermediate
Goal: Muscle Building
Days/Week: 4
Session Duration: 60 minutes
Equipment: Dumbbells, Resistance Bands
Injuries: None
Preferences: Prefer compound movements
"""

result = generate_workout_plan(test_input)
print("\nFinal Result:\n", result)