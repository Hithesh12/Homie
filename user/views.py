from django.shortcuts import render
from rest_framework.decorators import api_view

@api_view(http_method_names=['post'])
def registration(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password=request.POST['password']
        email=request.POST['email']
        created_by=request.POST['created_by']
        modified_by=request.POST['modified_by']
