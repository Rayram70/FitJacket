from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    path('profile/', views.profile_detail, name='profile_detail'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('user/<str:username>/', views.public_profile, name='public_profile'),

]
