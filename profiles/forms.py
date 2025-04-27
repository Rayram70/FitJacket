from allauth.account.forms import SignupForm
from django import forms
from .models import Profile




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


        return user
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'specialties', 'rate', 'available_times']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'specialties': forms.TextInput(attrs={'class': 'form-control'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_times': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
