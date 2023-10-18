from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, default="default.png")
    bio = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username
    
    @property
    def AvatarUrl(self):
        try:
            url = self.avatar.url
        except:
            url = ''
        return url
    def friends(self):
        sent_accepted = self.sent.filter(status = 'accepted')
        received_accepted = self.recived.filter(status = 'accepted')
        return list(sent_accepted)  + list(received_accepted)

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images")
    content = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
        get_latest_by = "created"

    def __str__(self):
        return f"posted by {self.author}"

    @property
    def ImageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    @property
    def likes(self):
        return self.like.likedBy.count()
        

class Like(models.Model):
    class Reaction(models.TextChoices):
        Like = 'like'
        Heart = 'heart'

    likedBy = models.ManyToManyField(Profile)
    likedPost = models.OneToOneField(Post, on_delete=models.CASCADE)
    reaction = models.TextField(max_length=9, choices=Reaction.choices, default=Reaction.Like)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  f"likes of {self.likedPost}" 
    
class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} commented on {self.post}"