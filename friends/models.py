from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FriendRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending' , 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_friend_requests")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_friend_requests")
    status = models.CharField(max_length=8 , choices=Status.choices, default=Status.PENDING)

    def __str__(self) :
        return f"{self.sender} send request {self.recipient}"
    
    def friends(self):
        return self.status == 'accepted'