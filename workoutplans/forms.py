from django import forms


class WorkoutPlanForm(forms.Form):
    FITNESS_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    FITNESS_GOALS = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Building'),
        ('strength', 'Strength Training'),
        ('endurance', 'Endurance'),
        ('flexibility', 'Flexibility/Mobility'),
        ('rehab', 'Rehabilitation'),
        ('sport', 'Sport-Specific'),
    ]

    EQUIPMENT_OPTIONS = [
        ('none', 'No Equipment'),
        ('dumbbells', 'Dumbbells'),
        ('resistance_bands', 'Resistance Bands'),
        ('yoga_mat', 'Yoga Mat'),
        ('kettlebells', 'Kettlebells'),
        ('pull_up_bar', 'Pull-up Bar'),
        ('full_gym', 'Full Gym Access'),
    ]

    # Personal Information
    age = forms.IntegerField(
        min_value=13,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Your current age"
    )

    fitness_level = forms.ChoiceField(
        choices=FITNESS_LEVELS,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='intermediate'
    )

    goal = forms.ChoiceField(
        choices=FITNESS_GOALS,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='muscle_gain'
    )

    # Workout Preferences
    days_per_week = forms.IntegerField(
        min_value=1,
        max_value=7,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="How many days per week can you work out?"
    )

    session_duration = forms.ChoiceField(
        choices=[(15, '15 min'), (30, '30 min'), (45, '45 min'),
                 (60, '60 min'), (90, '90 min')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial=45,
        help_text="Typical duration for each workout session"
    )

    equipment = forms.MultipleChoiceField(
        choices=EQUIPMENT_OPTIONS,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        help_text="Select all equipment you have access to"
    )

    # Special Considerations
    injuries = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'E.g., bad knee, lower back pain'
        }),
        help_text="List any injuries or physical limitations"
    )

    preferences = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'E.g., prefer bodyweight exercises, dislike running'
        }),
        help_text="Any specific preferences or dislikes"
    )

    additional_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Any other important information'
        }),
        help_text="Additional notes for your trainer"
    )

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 13:
            raise forms.ValidationError("You must be at least 13 years old to use this service.")
        return age

    def clean_days_per_week(self):
        days = self.cleaned_data['days_per_week']
        if days < 1 or days > 7:
            raise forms.ValidationError("Please enter a number between 1 and 7.")
        return days