from django.db import models
from django.contrib.auth.models import User

class Post(models.Model): 
    title = models.CharField(max_length=255)
    description = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)


    def __str__(self): 
        return self.title 

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:30]

    def is_reply(self):
        return self.parent is not None