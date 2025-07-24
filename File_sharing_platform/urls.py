from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("enter/", views.enter, name="enter"),
    path("register/", views.register, name="register"),
    path("logout/", views.user_logout, name="logout"),
    path("category/<str:category_name>/", views.posts_by_category, name='posts_by_category'),
    path("file/<str:title>/", views.file_detail, name='file_detail'),
]