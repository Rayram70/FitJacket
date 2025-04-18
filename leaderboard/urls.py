from django.urls import path
from . import views

urlpatterns = [
    path('', views.leaderboard_view, name='leaderboard'),
    path('my-badges/', views.my_badges_view, name='my_badges'),
]
