from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.PositiveIntegerField(default=0)
    love_count = models.PositiveIntegerField(default=0)
    funny_count = models.PositiveIntegerField(default=0)
    sad_count = models.PositiveIntegerField(default=0)
    shock_count = models.PositiveIntegerField(default=0)

    reactions_data = models.JSONField(default=dict)  # { "user_id": "reaction_type" }

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def __str__(self):
        return self.content[:30]

    def is_reply(self):
        return self.parent is not None

    def total_likes(self):
        return self.likes.count()
