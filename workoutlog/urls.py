from django.urls import path
from . import views

app_name = 'workoutlog'

urlpatterns = [
    path('log/', views.workout_create, name='workout_create'),
    path('my-workouts/', views.my_workouts, name='my_workouts'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
]
