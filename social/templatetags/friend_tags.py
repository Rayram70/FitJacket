from django import template
from django.db.models import Q  # ✅ Correct Q import
from social.models import FriendRequest

register = template.Library()

@register.filter
def has_sent_friend_request(from_user, to_user):
    return FriendRequest.objects.filter(from_user=from_user, to_user=to_user, accepted=False).exists()

@register.filter
def has_received_friend_request(to_user, from_user):
    return FriendRequest.objects.filter(from_user=from_user, to_user=to_user, accepted=False).exists()

@register.filter
def are_friends(user1, user2):
    return FriendRequest.objects.filter(
        Q(from_user=user1, to_user=user2) | Q(from_user=user2, to_user=user1),
        accepted=True
    ).exists()
