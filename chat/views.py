from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from core.models import Profile
from .models import Message

def chat(request):
    profile = get_object_or_404(Profile, user = request.user)
    friends = profile.friends()

    return render(request, 'chat/messenger.html', {'friends' : friends, 'profile' : profile})

@login_required
def chat_room(request, recipient_id):
    sender = get_object_or_404(Profile, user = request.user)
    recipient = get_object_or_404(Profile, id=recipient_id)
    friends = sender.friends()
    # Retrieve the chat messages between the current user and the recipient
    messages = Message.objects.filter(
        (Q(sender=sender) & Q(recipient=recipient)) |
        (Q(sender=recipient) & Q(recipient=sender))
    ).order_by('timestamp')

    context = {
        'recipient': recipient,
        'messages': messages,
        'friends' : friends,
        'sender' : sender,
        'profile' : sender
    }

    return render(request, 'chat/chat.html', context)

@login_required
def send_message(request):
    if request.method == 'POST':
        sender = get_object_or_404(Profile, user = request.user)
        recipient_id = request.POST.get('recipient_id')
        message_content = request.POST.get('message_content')

        recipient = get_object_or_404(Profile, id=recipient_id)

        # Create and save the message to the database
        message = Message(sender=sender, recipient=recipient, content=message_content)
        message.save()

        # Return a JSON response to indicate success
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})