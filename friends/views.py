from django.shortcuts import render
from django.views import View
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from core.models import Profile
from .models import FriendRequest

def friends(request):
    profile = Profile.objects.get(user = request.user)
    freinds = FriendRequest.objects.filter(Q(sender = profile) | Q(recipient = profile), status="accepted")
    return render(request, 'friends/friends.html',  {  
        "friends" : freinds,     
    })

def friend_request(request):
    profile = Profile.objects.get(user = request.user)
    friend_requests = FriendRequest.objects.filter(recipient = profile, status = 'pending')
    return render(request, 'friends/friend_request.html', {"friend_requests" : friend_requests,})

def sent_request(request):
    profile = Profile.objects.get(user = request.user)
    sent_requests = FriendRequest.objects.filter(sender = profile, status="pending")
    return render(request, 'friends/sent_request.html', {"sent_requests" : sent_requests,})

def find_friends(request):
    profile = Profile.objects.get(user = request.user)
    pass
    

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

