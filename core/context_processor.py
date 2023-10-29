from .forms import PostForm
from .models import Profile, Notification


def post_form(request):
    # Your form logic here
    form = PostForm()
    return {'post_form': form}

def count(request):
    user = request.user
    count = 0
    if user.is_authenticated:
        profile = Profile.objects.get(user = user)
        notifications = Notification.objects.filter(notify_to = profile, is_read = False)
        count = notifications.count()
    return {'count' : count}