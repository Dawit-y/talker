from django.db import models
from core.models import Profile

class FriendRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending' , 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sent")
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="recived")
    status = models.CharField(max_length=8 , choices=Status.choices, default=Status.PENDING)

    def __str__(self) :
        return f"{self.sender} send request to {self.recipient}"
    
    def name():
        pass