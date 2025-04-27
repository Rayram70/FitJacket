# messaging/forms.py
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Type your message...'}),
        }
