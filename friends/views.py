from django.shortcuts import render
from django.views import View
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from .models import FriendRequest
import json

# Create your views here.



def send_friend_request(request, **kwargs):
        sender = User.objects.get(id = request.user.id)
        recipient = User.objects.get(id=kwargs['id'])
        status = "none"
        try:
            already_sent_request = FriendRequest.objects.get(sender=sender, recipient=recipient)
            status = already_sent_request.status
            
        except:   
            friend_request = FriendRequest.objects.create(sender=sender,recipient=recipient)
            status = friend_request.status 
        # response = HttpResponse(status=302)
        # response["Location"] = "/"
        return JsonResponse({"status" : status})

def notification(request) :
    error = "nothing"

    friend_requests = FriendRequest.objects.filter(recipient = request.user, status = 'pending')
    sent_request = FriendRequest.objects.filter(sender = request.user, status="pending")
    freinds = FriendRequest.objects.filter(Q(sender = request.user) | Q(recipient = request.user), status="accepted")
    print( freinds)
    return render(request, 'chat/notification.html' , 
        {
            "friend_requests" : friend_requests,
            "sent_requests" : sent_request,
            "friends" : freinds,
            "error" : error
        }
        )

