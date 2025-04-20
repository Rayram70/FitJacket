from allauth.account.forms import SignupForm
from django import forms

from trainers.models import Trainer  # Add this import at the top

class CustomSignupForm(SignupForm):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('trainer', 'Trainer'),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    def save(self, request):
        user = super().save(request)
        role = self.cleaned_data['role']
        user.profile.role = role
        user.profile.save()

        # ✅ If the role is trainer, create a Trainer instance
        if role == 'trainer':
            Trainer.objects.create(user=user)

        return user
