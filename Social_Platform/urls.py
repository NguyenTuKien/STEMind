from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('explore/', views.explore, name='explore'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('liked/', views.liked_posts, name='liked_posts'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
] 