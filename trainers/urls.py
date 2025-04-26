from django.urls import path
from . import views

app_name = 'trainers'

urlpatterns = [
    path('profile/', views.trainer_profile, name='trainer_profile'),
    path('<int:trainer_id>/', views.trainer_detail, name='trainer_detail'),
    path('book/<int:trainer_id>/', views.book_session, name='book_session'),
    path('dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
    path('connect/<int:trainer_id>/', views.connect_trainer, name='connect_trainer'),
    path('clients/<int:client_id>/', views.client_dashboard, name='client_dashboard'),

    path('clients/', views.client_list, name='client_list'),

]
