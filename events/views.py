from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from django.contrib.auth.decorators import login_required

def event_list(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.participants.add(request.user)
    return redirect('event_detail', event_id=event.id)

@login_required
def leave_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.participants.remove(request.user)
    return redirect('event_detail', event_id=event.id)
