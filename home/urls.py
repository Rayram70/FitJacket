
from . import views
from django.urls import path, include
urlpatterns = [
    path('', views.index, name='home.index'),
    path('about/', views.about, name='home.about'),
    path('feed/', views.feed, name='trainer_feed'),  # name stays the same so the template doesn't break

]

