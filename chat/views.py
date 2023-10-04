from django.shortcuts import render
from core.models import Profile


def chat(request):
    profile = Profile.objects.get(user = request.user)
    return render(request, "chat/messenger.html", {'profile' : profile})