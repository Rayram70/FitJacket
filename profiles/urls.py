from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    path('profile/', views.profile_detail, name='profile_detail'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('user/<str:username>/', views.public_profile, name='public_profile'),
    path('connect-trainer/<int:trainer_id>/', views.connect_trainer, name='connect_trainer'),
    path('disconnect-trainer/', views.disconnect_trainer, name='disconnect_trainer'),
    path('remove-client/<int:client_id>/', views.remove_client, name='remove_client'),

]
