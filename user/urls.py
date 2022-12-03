from django.urls import path
from .import views

urlpatterns = [
    path('register',views.registration),
    path('login',views.login),
    path('list',views.userlist),
    path('fetch',views.edit)
]