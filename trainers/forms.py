from django import forms
from .models import Trainer
import datetime
from .models import TrainerComment

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
        ('12:00', '12:00 AM'),
        ('01:00', '1:00 AM'),
        ('02:00', '2:00 AM'),
        ('03:00', '3:00 AM'),
        ('04:00', '4:00 AM'),
        ('05:00', '5:00 AM'),
        ('06:00', '6:00 AM'),
        ('07:00', '7:00 AM'),
        ('08:00', '8:00 AM'),
        ('09:00', '9:00 AM'),
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('14:00', '2:00 PM'),
        ('15:00', '3:00 PM'),
        ('16:00', '4:00 PM'),
        ('17:00', '5:00 PM'),
        ('18:00', '6:00 PM'),
        ('19:00', '7:00 PM'),
        ('20:00', '8:00 PM'),
        ('21:00', '9:00 PM'),
        ('22:00', '10:00 PM'),
        ('23:00', '11:00 PM'),
    ]

    time_slot = forms.ChoiceField(
        choices=TIME_SLOTS,
        widget=forms.RadioSelect,
        label="Select a Time Slot"
    )


class TrainerCommentForm(forms.ModelForm):
    class Meta:
        model = TrainerComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Write your review...'})
        }
