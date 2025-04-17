
from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('post/', views.create_post, name='create_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
]
