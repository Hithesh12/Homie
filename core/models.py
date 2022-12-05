from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    created = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=255)
    premium_user=models.BooleanField(default=False)
    price=models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone']

    def __str__(self) -> str:
        return self.username
