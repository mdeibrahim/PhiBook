from django.conf import settings
from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField()
    image = models.ImageField(upload_to='posts/',blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Post by {self.user.email} on {self.created_at}"
    
    @property
    def total_likes(self):
        return self.likes.filter(reaction_type='like').count()

    @property
    def total_unlikes(self):
        return self.likes.filter(reaction_type='unlike').count()
    
    @property
    def total_comments(self):
        return self.comments.count()

    

class Like(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('unlike', 'Unlike'),
    ] 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    reaction_type = models.CharField(max_length=7, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_like')
        ]


    def __str__(self):
        return f"{self.reaction_type} by {self.user.email} on {self.post.id} at {self.created_at}"
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.email} on {self.post.id} at {self.created_at}"
    
