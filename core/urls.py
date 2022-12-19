from django.urls import path
from .import views

urlpatterns = [
    path('frie/', views.friends, name='friends'),
    path('post', views.post, name='post'),
    path('feed', views.feed, name='feed'),
    path('like/<int:pk>/', views.likes, name='like'),
    path('upload/', views.Image, name='image'),
    path('delete/<int:pk>',views.ImageDel,name='imgdelete'),
    path('imagelike/<int:pk>/',views.likeimage,name='likeimage'),
    path('profile/',views.Profile,name='profile')
]
