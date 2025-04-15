from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.workout_create, name='workout_create'),
    path('my/', views.my_workouts, name='my_workouts'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
]
