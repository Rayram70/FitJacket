
from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    logged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='logged_workouts')
    date = models.DateField()
    activity = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity} for {self.user.username} on {self.date}"
class Goal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    monthly_workout_goal = models.PositiveIntegerField(default=0)
    monthly_minutes_goal = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s goal"