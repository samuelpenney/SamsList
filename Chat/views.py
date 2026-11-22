from django.shortcuts import render
def lobby(request):
    return render(request, 'Chat/lobby.html')  # entry page, no dynamic data needed
def room(request, room_name):
    # room_name arrives from the URL - traced below
    return render(request, 'Chat/room.html', {'room_name': room_name})