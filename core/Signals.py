from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from friends.models import FriendRequest
from .models import Profile, Notification

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_delete, sender=Profile)
def delete_profile(sender, instance, **kwargs):
    instance.user.delete()

@receiver(post_save, sender = FriendRequest)
def create_request_notification(sender, instance, created , **kwargs):
    cn = ContentType.objects.get_for_model(FriendRequest)
    id = instance.id
    if instance.status == "pending":
        Notification.objects.create(
            notify_to = instance.recipient, 
            content = f"{instance.sender} sent you friend request", 
            content_type = cn, 
            object_id = id )
    elif instance.status == "rejected":
        Notification.objects.create(
            notify_to = instance.sender, 
            content = f"{instance.recipient} rejected your friend request", 
            content_type = cn, 
            object_id = id )
    elif instance.status == "accepted":
        Notification.objects.create(
            notify_to = instance.sender, 
            content = f"{instance.recipient} accepted your friend request", 
            content_type = cn, 
            object_id = id )
    else:
        print("something in signals")
