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
    friends=models.ManyToManyField("User",blank=True)
  
   
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone']

    def __str__(self) -> str:
        return self.username

class Friend_Request(models.Model):
    main_user=models.ForeignKey(User,related_name='main_user',on_delete=models.CASCADE)
    friend_user=models.ForeignKey(User,related_name="fiend_user",on_delete=models.CASCADE)
    friends=models.BooleanField(default=False)

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    title=models.CharField(max_length=255)
    text=models.TextField(max_length=255)
    post=models.DateTimeField(auto_now_add=True)
    like=models.ManyToManyField(User,related_name='post')




    

