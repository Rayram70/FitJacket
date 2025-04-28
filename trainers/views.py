from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from workoutlog.models import Workout
from .forms import BookingForm, TrainerCommentForm, TrainerProfileForm
from .models import SessionBooking, TrainerComment
from datetime import datetime
from django.db.models import Sum



@login_required
def trainer_profile(request):
    if request.user.profile.role != 'trainer':
        return HttpResponseForbidden("You are not registered as a trainer.")

    profile = request.user.profile

    if request.method == 'POST':
        form = TrainerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('trainers:trainer_profile')
    else:
        form = TrainerProfileForm(instance=profile)

    return render(request, 'profiles/profile_edit.html', {'form': form})  # Unified under profiles app


@login_required
def trainer_detail(request, trainer_id):
    trainer_profile = get_object_or_404(Profile, id=trainer_id, role='trainer')
    comments = trainer_profile.comments.select_related('user').order_by('-created_at')

    if request.method == 'POST':
        form = TrainerCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.trainer = trainer_profile
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment posted successfully.")
            return redirect('trainers:trainer_detail', trainer_id=trainer_profile.id)
    else:
        form = TrainerCommentForm()

    return render(request, 'trainers/trainer_detail.html', {
        'trainer': trainer_profile,
        'form': form,
        'comments': comments,
    })


@login_required
def book_session(request, trainer_id):
    trainer_profile = get_object_or_404(Profile, id=trainer_id, role='trainer')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            SessionBooking.objects.create(
                user=request.user,
                trainer_profile=trainer_profile,
                date=form.cleaned_data['date'],
                time_slot=form.cleaned_data['time_slot']
            )
            messages.success(request, "Session booked successfully!")
            return redirect('trainers:trainer_detail', trainer_id=trainer_profile.id)
    else:
        form = BookingForm()

    return render(request, 'trainers/book_session.html', {
        'trainer': trainer_profile,
        'form': form
    })


@login_required
def trainer_dashboard(request):
    if request.user.profile.role != 'trainer':
        return HttpResponseForbidden("You are not registered as a trainer.")

    trainer_profile = request.user.profile
    sessions = trainer_profile.sessions.all().order_by('date', 'time_slot')

    return render(request, 'trainers/trainer_dashboard.html', {
        'sessions': sessions
    })


@login_required
def connect_trainer(request, trainer_id):
    trainer_profile = get_object_or_404(Profile, id=trainer_id, role='trainer')

    if request.method == 'POST':
        if request.user.profile.role == 'user' and not request.user.profile.connected_trainer:
            request.user.profile.connected_trainer = trainer_profile
            request.user.profile.save()
            messages.success(request, f"You are now connected with {trainer_profile.user.username}!")
        else:
            messages.error(request, "You are already connected to a trainer.")

    return redirect('trainers:trainer_detail', trainer_id=trainer_profile.id)


@login_required
def client_list(request):
    if not request.user.profile.role == 'trainer':
        return HttpResponseForbidden("You are not authorized to view this page.")

    trainer_profile = request.user.profile
    clients = trainer_profile.clients.all()

    return render(request, 'trainers/client_list.html', {'clients': clients})


@login_required
def client_dashboard(request, client_id):
    client = get_object_or_404(Profile, id=client_id, role='user', connected_trainer=request.user.profile)

    workouts = Workout.objects.filter(user=client.user).order_by('-date')

    today = datetime.today()
    monthly_workouts = workouts.filter(date__year=today.year, date__month=today.month)

    total_workouts_month = monthly_workouts.count()
    total_minutes_month = monthly_workouts.aggregate(total=Sum('duration'))['total'] or 0

    # build data for chart
    chart_labels = [w.date.strftime('%b %d') for w in monthly_workouts]
    chart_data = [w.duration for w in monthly_workouts]

    return render(request, 'trainers/client_dashboard.html', {
        'client': client,
        'workouts': workouts,
        'total_workouts_month': total_workouts_month,
        'total_minutes_month': total_minutes_month,
        'chart_labels': chart_labels,
        'chart_data': chart_data
    })
