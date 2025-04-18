from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from .models import UserBadge

def leaderboard_view(request):
    leaderboard = (
        User.objects.annotate(
            total_minutes=Sum('workouts__duration'),
            total_workouts=Count('workouts')
        )
        .filter(total_minutes__isnull=False)
        .order_by('-total_minutes')[:20]
    )
    return render(request, 'leaderboard/leaderboard.html', {'leaderboard': leaderboard})

def my_badges_view(request):
    badges = UserBadge.objects.filter(user=request.user)
    return render(request, 'leaderboard/my_badges.html', {'badges': badges})
