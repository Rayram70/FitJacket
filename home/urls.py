
from . import views
from django.urls import path, include
from .views import motivational_message
urlpatterns = [
    path('', views.index, name='home.index'),
    path('about/', views.about, name='home.about'),
    path('feed/', views.feed, name='trainer_feed'),  # name stays the same so the template doesn't break

    path('api/motivation/', motivational_message, name='motivational_message'),

]

