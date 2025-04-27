from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('trainer', 'Trainer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)

    # Trainer-specific
    specialties = models.CharField(max_length=255, blank=True)
    rate = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    available_times = models.TextField(blank=True)

    # 👇 Add this
    connected_trainer = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='clients',
        limit_choices_to={'role': 'trainer'}
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"
