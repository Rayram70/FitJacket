from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('thread/<int:user_id>/', views.thread, name='thread'),
    path('send/<int:user_id>/', views.send_message, name='send_message'),
    path('new/', views.new_message, name='new_message'),  # 👈 Add this!
]