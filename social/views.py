from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Sum, Q
from django.utils.timezone import now


from .models import Post, FriendRequest
from .forms import PostForm, CommentForm
from workoutlog.models import Workout

# --- SOCIAL FEED ---
@login_required
def feed(request):
    posts = Post.objects.select_related('user', 'user__profile').prefetch_related('comments__user').order_by('-created_at')
    stats = {}
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

    comment_form = CommentForm()
    return render(request, 'social/feed.html', {
        'posts': posts,
        'stats': stats,
        'comment_form': comment_form
    })

# --- CREATE A POST ---
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

# --- ADD COMMENT ---
@require_POST
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
    return redirect('social:feed')

# --- SEND FRIEND REQUEST ---
@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    if to_user != request.user:
        FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    return redirect('profiles:public_profile', username=to_user.username)

# --- ACCEPT FRIEND REQUEST ---
@login_required
def accept_friend_request(request, request_id):
    fr = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    fr.accepted = True
    fr.save()
    return redirect('profiles:public_profile', username=fr.from_user.username)

# --- DECLINE FRIEND REQUEST ---
@login_required
def decline_friend_request(request, request_id):
    fr = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    fr.delete()
    return redirect('profiles:public_profile', username=fr.from_user.username)


@login_required
def friends_list(request):
    # Fetch all users who are friends with the current user
    friends = User.objects.filter(
        Q(sent_requests__to_user=request.user, sent_requests__accepted=True) |
        Q(received_requests__from_user=request.user, received_requests__accepted=True)
    ).distinct()

    # Fetch all pending friend requests received
    pending_requests = FriendRequest.objects.filter(
        to_user=request.user, accepted=False
    )

    return render(request, 'social/friends_list.html', {
        'friends': friends,
        'pending_requests': pending_requests
    })


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'total_likes': post.likes.count()
    })