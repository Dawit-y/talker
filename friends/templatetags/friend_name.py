from django import template
from django.shortcuts import get_object_or_404
from core.models import Profile

register = template.Library()

@register.filter
def friend_name(model_instance, request):
    profile = get_object_or_404(Profile, user = request.user)
    if model_instance.sender == profile:
        return model_instance.recipient
    else:
        return model_instance.sender
