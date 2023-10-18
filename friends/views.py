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
    # freinds = FriendRequest.objects.filter(Q(sender = profile) | Q(recipient = profile), status="accepted")
    friends = profile.friends()
    return render(request, 'friends/friends.html',  {  
        "friends" : friends,     
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
    profile = Profile.objects.prefetch_related('sent', 'recived').get(user = request.user)
    recipient_profiles = [request.recipient for request in profile.sent.all()]
    sender_profiles = [request.sender for request in profile.recived.all()]
    profiles = Profile.objects.exclude(id = profile.id)
    recommendations = [profile for profile in profiles if profile not in recipient_profiles + sender_profiles]
   
    return render(request, 'friends/find_friends.html', {'recommendations' : recommendations})
    

def send_friend_request(request, **kwargs):
    sender = Profile.objects.get(user = request.user)
    recipient_user = User.objects.get(id=kwargs['id'])
    recipient = Profile.objects.get(user = recipient_user)
     
    friend_request = FriendRequest.objects.create(sender=sender,recipient=recipient)
    status = friend_request.status 
    print("new request being sent")

    return JsonResponse({"status" : status})

def accept_request(request, **kwargs):
    request_obj = FriendRequest.objects.get(id = kwargs['id'])
    request_obj.status = 'accepted'
    request_obj.save()
    return JsonResponse({"ACCepted" : request_obj.status})

def reject_request(request, **kwargs):
    request_obj = FriendRequest.objects.get(id = kwargs['id'])
    request_obj.status = 'rejected'
    request_obj.delete()
    return JsonResponse({"Rejected" : request_obj.status})

def cancel_request(request, **kwargs):
    request_obj = FriendRequest.objects.get(id = kwargs['id'])
    request_obj.delete()
    return JsonResponse({"Cancelled" : "cancelled"})


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

