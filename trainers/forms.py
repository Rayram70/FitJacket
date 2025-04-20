from django import forms
from .models import Trainer
import datetime


class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['bio', 'specialties', 'rate', 'available_times']



class BookingForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=datetime.date.today,
        label="Select a Date"
    )

    TIME_SLOTS = [
        ('09:00', '9:00 AM'),
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('14:00', '2:00 PM'),
        ('15:00', '3:00 PM'),
        ('16:00', '4:00 PM'),
    ]

    time_slot = forms.ChoiceField(
        choices=TIME_SLOTS,
        widget=forms.RadioSelect,
        label="Select a Time Slot"
    )

