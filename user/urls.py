from django.urls import path
from .import views

urlpatterns = [
    path('register',views.registration,name='registration'),
    path('login',views.login,name='login'),
    path('list',views.userlist,name='userlist'),
    path('fetch',views.edit,name='edit'),
    
]