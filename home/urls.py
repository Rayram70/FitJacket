
from . import views
from django.urls import path, include
urlpatterns = [
    path('', views.index, name='home.index'),
    path('about/', views.about, name='home.about'),



]

