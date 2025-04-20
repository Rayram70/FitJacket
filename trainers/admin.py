from django.contrib import admin
from .models import Trainer

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('user', 'rate', 'specialties')
    search_fields = ('user__username', 'specialties')
