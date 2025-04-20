from trainers.models import Trainer
from django.shortcuts import render

def index(request):
    template_data = {}
    template_data['title'] = 'Fit Jacket'
    return render(request, 'home/index.html', {'template_data': template_data})
def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {'template_data': template_data})

def feed(request):
    trainers = Trainer.objects.select_related('user').all()
    return render(request, 'home/feed.html', {'trainers': trainers})

