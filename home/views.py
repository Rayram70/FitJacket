from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from profiles.models import Profile  # 🛠 import Profile instead!
from messaging.models import Message

@login_required
def index(request):
    unread_count = Message.objects.filter(recipient=request.user, is_read=False).count()

    return render(request, 'home/index.html', {
        'template_data': {
            'title': 'FitJacket',
        },
        'unread_count': unread_count
    })

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {'template_data': template_data})

def feed(request):
    # 🛠 Get all profiles where role = 'trainer'
    trainers = Profile.objects.filter(role='trainer').select_related('user')
    return render(request, 'home/feed.html', {'trainers': trainers})
