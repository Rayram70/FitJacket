from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_events')
    participants = models.ManyToManyField(User, related_name='events_joined', blank=True)

    def __str__(self):
        return f"{self.title} at {self.location} on {self.date.strftime('%Y-%m-%d')}"
