from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def room(request):
    return render(request, 'chat/room.html', {
        'room_name': 'comunity'
    })
