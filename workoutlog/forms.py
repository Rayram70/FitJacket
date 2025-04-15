from django import forms
from .models import Workout, Goal

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['date', 'activity', 'duration', 'notes']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'activity': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user')
        super().__init__(*args, **kwargs)


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['monthly_workout_goal', 'monthly_minutes_goal']
        widgets = {
            'monthly_workout_goal': forms.NumberInput(attrs={'class': 'form-control'}),
            'monthly_minutes_goal': forms.NumberInput(attrs={'class': 'form-control'}),
        }