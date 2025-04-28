from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from .forms import ProfileForm

@login_required
def profile_detail(request):
    return render(request, 'profiles/profile_detail.html', {
        'profile': request.user.profile
    })

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profiles:profile_detail')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/profile_edit.html', {
        'form': form
    })


@login_required
def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile  # assuming you have a OneToOne relation
    return render(request, 'profiles/public_profile.html', {'user_profile': user, 'profile': profile})

@login_required
def connect_trainer(request, trainer_id):
    trainer = get_object_or_404(Profile, id=trainer_id, role='trainer')

    if request.user.profile.role != 'user':
        return HttpResponseForbidden('Only users can connect to trainers.')

    # Connect
    request.user.profile.connected_trainer = trainer
    request.user.profile.save()

    return redirect('profiles:profile_detail')


@login_required
def disconnect_trainer(request):
    profile = request.user.profile

    if profile.connected_trainer:
        profile.connected_trainer = None
        profile.save()

    # 👇 Smart redirect: back to where the request came from, or fallback
    next_url = request.META.get('HTTP_REFERER', 'profiles:profile_detail')
    return redirect(next_url)


@login_required
def remove_client(request, client_id):
    trainer = request.user.profile
    if trainer.role != 'trainer':
        return HttpResponseForbidden('Only trainers can remove clients.')

    client_profile = get_object_or_404(Profile, id=client_id, role='user', connected_trainer=trainer)
    client_profile.connected_trainer = None
    client_profile.save()

    return redirect('trainers:client_list')

