from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from .forms import MessageForm
from profiles.models import Profile  # important
from django.db.models import Q
from django.db import models
from django.http import HttpResponseForbidden



@login_required
def inbox(request):
    # Get all users who sent OR received a message with this user
    conversations = Message.objects.filter(
        models.Q(sender=request.user) | models.Q(recipient=request.user)
    ).order_by('-created_at')

    return render(request, 'messaging/inbox.html', {'conversations': conversations})

@login_required
def thread(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    my_profile = request.user.profile
    other_profile = other_user.profile

    # 🔥 Important: Allow messaging only if trainer and client are connected
    if not (
        (my_profile.role == 'trainer' and other_profile.connected_trainer == my_profile) or
        (my_profile.role == 'user' and my_profile.connected_trainer == other_profile)
    ):
        return HttpResponseForbidden('You can only message your connected trainer or client.')

    messages = Message.objects.filter(
        (Q(sender=request.user, recipient=other_user) | Q(sender=other_user, recipient=request.user))
    ).order_by('created_at')

    Message.objects.filter(sender=other_user, recipient=request.user, is_read=False).update(is_read=True)

    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = other_user
            msg.save()
            return redirect('messaging:thread', user_id=other_user.id)

    return render(request, 'messaging/thread.html', {
        'messages': messages,
        'other_user': other_user,
        'form': form,
    })


@login_required
def send_message(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    my_profile = request.user.profile
    other_profile = other_user.profile

    # 🔥 Check if they are allowed to message each other (client ↔ trainer)
    if not (
        (my_profile.role == 'trainer' and other_profile.connected_trainer == my_profile) or
        (my_profile.role == 'user' and my_profile.connected_trainer == other_profile)
    ):
        return HttpResponseForbidden('You are not allowed to message this user.')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = other_user
            message.save()
            return redirect('messaging:thread', user_id=other_user.id)
    else:
        form = MessageForm()

    return render(request, 'messaging/send_message.html', {'form': form, 'other_user': other_user})

@login_required
def new_message(request):
    profile = request.user.profile

    # Start with empty list
    users = []

    # Trainer can message their clients
    if profile.role == 'trainer':
        users = [client.user for client in profile.clients.all()]

    # User can message their connected trainer
    elif profile.connected_trainer:
        users.append(profile.connected_trainer.user)

    # 💬 Plus add friends if you have a friend system
    if hasattr(request.user, 'friends'):
        users += [friend for friend in request.user.friends.all()]

    # Remove duplicates (if someone is both a client *and* a friend)
    users = list(set(users))

    return render(request, 'messaging/new_message.html', {'users': users})