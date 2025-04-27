from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import WorkoutGroup, GroupMembership
from .forms import WorkoutGroupForm
from collections import defaultdict

@login_required
def create_group(request):
    if request.method == 'POST':
        form = WorkoutGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            GroupMembership.objects.create(user=request.user, group=group)
            return redirect('groups:group_list')
    else:
        form = WorkoutGroupForm()
    return render(request, 'groups/create_group.html', {'form': form})

@login_required
def join_group(request, group_id):
    group = get_object_or_404(WorkoutGroup, id=group_id)
    GroupMembership.objects.get_or_create(user=request.user, group=group)

    # Redirect back to the group list instead of group detail
    return redirect('groups:group_list')

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(WorkoutGroup, id=group_id)
    members = GroupMembership.objects.filter(group=group)
    return render(request, 'groups/group_detail.html', {'group': group, 'members': members})

@login_required
def group_list(request):
    groups = WorkoutGroup.objects.all()
    user_memberships = GroupMembership.objects.filter(user=request.user).values_list('group_id', flat=True)

    # Map: group_id -> list of usernames
    group_members = defaultdict(list)
    all_memberships = GroupMembership.objects.select_related('user', 'group')
    for membership in all_memberships:
        group_members[membership.group_id].append(membership.user.username)

    return render(request, 'groups/group_list.html', {
        'groups': groups,
        'user_memberships': user_memberships,
        'group_members': group_members
    })

@login_required
def leave_group(request, group_id):
    group = get_object_or_404(WorkoutGroup, id=group_id)
    GroupMembership.objects.filter(user=request.user, group=group).delete()
    return redirect('groups:group_list')
