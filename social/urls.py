
from django.urls import path
from . import views
from profiles import views as profile_views

app_name = 'social'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('post/', views.create_post, name='create_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('send-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline-request/<int:request_id>/', views.decline_friend_request, name='decline_friend_request'),

    path('user/<str:username>/', profile_views.public_profile, name='public_profile'),

    path('friends/', views.friends_list, name='friends_list'),






]
