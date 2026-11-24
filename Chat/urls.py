from django.urls import path
from . import views

urlpatterns = [
    path('', views.lobby, name='lobby'),            # /chat/
    path('<slug:room_name>/', views.room, name='room'),  # /chat/friends/
]