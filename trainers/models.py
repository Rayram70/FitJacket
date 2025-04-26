from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile


class SessionBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='session_bookings')
    trainer_profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='sessions', null=True, blank=True)  # <- Added null=True, blank=True
    date = models.DateField()
    time_slot = models.CharField(max_length=10)
    booked_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} booked {self.trainer_profile.user.username} on {self.date} at {self.time_slot}"


class TrainerComment(models.Model):
    trainer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')  # ⬅️ Link to Profile
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Who posted the comment
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.trainer.user.username}"
