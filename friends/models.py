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

    def __str__(self):
        return f"{self.sender} send request to {self.recipient}"
    
    def save(self, *args, **kwargs):
        already_sent =  FriendRequest.objects.filter(sender = self.sender, recipient = self.recipient, status = self.status)
        if already_sent.count() == 0:
            return super().save(*args, **kwargs)
        else:
            raise Exception("There is already friend request instance between you two")


        