from django.contrib import admin
from .models import WorkoutGroup, GroupMembership

admin.site.register(WorkoutGroup)
admin.site.register(GroupMembership)
