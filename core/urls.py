from django.urls import path
from .import views

urlpatterns = [
    path('frie/',views.friends,name='friends'),
    path('post',views.post,name='post'),
    path('feed',views.feed,name='feed')
]