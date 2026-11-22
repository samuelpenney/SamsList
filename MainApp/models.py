# Create your models here.
from django.db import models
from django.urls import reverse 
from django.conf import settings
from django.core.validators import RegexValidator
 
class Post(models.Model): 
    title = models.CharField(max_length=200) 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10)
    body = models.TextField() 
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):  
        return reverse("post_detail", kwargs={"pk": self.pk})
