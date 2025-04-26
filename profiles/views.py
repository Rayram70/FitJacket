from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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
            return redirect('profile_detail')
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

