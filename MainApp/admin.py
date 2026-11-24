from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post 
class PostAdmin(admin.ModelAdmin):  # new 
    list_display = ( 
    "title", 
    "author",
    "zip_code",
    "body", 
) 
admin.site.register(Post, PostAdmin)