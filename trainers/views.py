
# Create your views here.

from .forms import TrainerProfileForm
from .models import Trainer

from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BookingForm
from .models import SessionBooking

from django.contrib.auth.decorators import login_required



@login_required
def trainer_profile(request):
    # Check if this user has a Trainer profile
    if not hasattr(request.user, 'trainer'):
        return HttpResponseForbidden("You are not registered as a trainer.")

    trainer = request.user.trainer

    if request.method == 'POST':
        form = TrainerProfileForm(request.POST, instance=trainer)
        if form.is_valid():
            form.save()
            return redirect('trainer_profile')
    else:
        form = TrainerProfileForm(instance=trainer)

    return render(request, 'trainers/profile.html', {'form': form})



def trainer_detail(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    return render(request, 'trainers/trainer_detail.html', {'trainer': trainer})


def book_session(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            SessionBooking.objects.create(
                user=request.user,
                trainer=trainer,
                date=form.cleaned_data['date'],
                time_slot=form.cleaned_data['time_slot']
            )
            messages.success(request, "Session booked successfully!")
            return redirect('book_session', trainer_id=trainer.id)
    else:
        form = BookingForm()

    return render(request, 'trainers/book_session.html', {
        'trainer': trainer,
        'form': form
    })


@login_required
def trainer_dashboard(request):
    trainer = get_object_or_404(Trainer, user=request.user)
    sessions = trainer.sessions.all().order_by('date', 'time_slot')  # related_name="sessions"

    return render(request, 'trainers/trainer_dashboard.html', {
        'sessions': sessions
    })

