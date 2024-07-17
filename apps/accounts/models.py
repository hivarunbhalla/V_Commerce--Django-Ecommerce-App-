from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from ..base.models import BaseModel



class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    address = models.CharField(max_length=255, blank=True, null=True)
    email_token = models.CharField(max_length=100 , null=True , blank=True)
    is_email_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username
