from django.db import models
from django.contrib.auth.models import User


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    specialties = models.CharField(max_length=255, blank=True)
    rate = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    available_times = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class SessionBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='session_bookings')
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    time_slot = models.CharField(max_length=10)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booked {self.trainer.user.username} on {self.date} at {self.time_slot}"


class TrainerComment(models.Model):
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.trainer.user.username}"


