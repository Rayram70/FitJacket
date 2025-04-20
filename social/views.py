from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm, CommentForm
from django.db.models import Sum
from django.utils.timezone import now
from workoutlog.models import Workout
from django.views.decorators.http import require_POST


@login_required
def feed(request):
    posts = Post.objects.select_related('user', 'user__profile').prefetch_related('comments__user').order_by('-created_at')
    stats = {}
    comment_form = CommentForm()

    today = now().date()
    for post in posts:
        if post.include_dashboard:
            month_workouts = Workout.objects.filter(
                user=post.user,
                date__year=today.year,
                date__month=today.month
            )
            stats[post.id] = {
                'count': month_workouts.count(),
                'minutes': month_workouts.aggregate(total=Sum('duration'))['total'] or 0
            }

    return render(request, 'social/feed.html', {
        'posts': posts,
        'stats': stats,
        'comment_form': comment_form
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('social:feed')
    else:
        form = PostForm()

    return render(request, 'social/create_post.html', {'form': form})

@require_POST
@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
    return redirect('social:feed')