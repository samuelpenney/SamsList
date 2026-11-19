from django.contrib.auth.models import AbstractUser
from django.db import models 

class CustomUser(AbstractUser): 
    zip = models.PositiveIntegerField(null=True, blank=True)