from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import render, redirect
from django.db.models.functions import TruncMonth
from django.utils.timezone import now



from .forms import WorkoutForm, GoalForm
from .models import Workout, Goal
import calendar

from leaderboard.models import UserProfile, Badge, UserBadge

from workoutplans.models import WorkoutPlan  # ✅ you need this import


@login_required
def user_dashboard(request):
    workouts = Workout.objects.filter(user=request.user)

    # Get or create user's goal
    goal, created = Goal.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        goal_form = GoalForm(request.POST, instance=goal)
        if goal_form.is_valid():
            goal_form.save()
            return redirect('user_dashboard')
    else:
        goal_form = GoalForm(instance=goal)

    # ✅ Fetch saved workout plans for this user
    saved_plans = WorkoutPlan.objects.filter(user=request.user).order_by('-created_at')

    # Chart + stats logic...
    monthly_data = (
        workouts
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(
            total_workouts=Count('id'),
            total_minutes=Sum('duration')
        )
        .order_by('month')
    )

    labels = [calendar.month_name[data['month'].month] for data in monthly_data]
    workouts_per_month = [data['total_workouts'] for data in monthly_data]
    minutes_per_month = [data['total_minutes'] for data in monthly_data]

    today = now().date()
    current_month_workouts = workouts.filter(date__month=today.month, date__year=today.year)
    this_month_total = current_month_workouts.count()
    this_month_minutes = current_month_workouts.aggregate(Sum('duration'))['duration__sum'] or 0

    stats = {
        'total': workouts.count(),
        'minutes': workouts.aggregate(total=Sum('duration'))['total'] or 0,
        'frequent': workouts.values('activity')
                            .annotate(freq=Count('activity'))
                            .order_by('-freq')
                            .first(),
        'recent': workouts.order_by('-date')[:5],
        'chart': {
            'labels': labels,
            'workouts': workouts_per_month,
            'minutes': minutes_per_month,
        },
        'this_month': {
            'workouts': this_month_total,
            'minutes': this_month_minutes
        },
        'goal': goal
    }

    return render(request, 'workoutlog/user_dashboard.html', {
        'stats': stats,
        'goal_form': goal_form,
        'saved_plans': saved_plans,  # ✅ Pass it cleanly
    })




def my_workouts(request):
    workouts = Workout.objects.filter(user=request.user).order_by('-date')
    return render(request, 'workoutlog/workout_list.html', {'workouts': workouts})

@login_required
def workout_create(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST, current_user=request.user)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.logged_by = request.user
            workout.save()

            # ✅ Award points
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.points += 10  # You can tweak this value if needed
            profile.save()

            # ✅ Award badges if thresholds met
            earned_badges = UserBadge.objects.filter(user=request.user).values_list('badge', flat=True)
            available_badges = Badge.objects.exclude(id__in=earned_badges)
            for badge in available_badges:
                if profile.points >= badge.threshold:
                    UserBadge.objects.create(user=request.user, badge=badge)

            return redirect('workoutlog:my_workouts')  # ✅ Use namespaced URL if needed
    else:
        form = WorkoutForm(current_user=request.user)

    return render(request, 'workoutlog/workout_form.html', {'form': form})