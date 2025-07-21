from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Reaction(models.Model):
    class ReactionType(models.TextChoices):
        LIKE = 'like', _('1. Like')
        DISLIKE = 'dislike', _('2. Dislike')
        LOVE = 'love', _('3. Love')
        FUNNY = 'funny', _('4. Funny')
        SAD = 'sad', _('5. Sad')
        SHOCK = 'shock', _('6. Shock')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='reactions', on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=ReactionType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Only one reaction per user per post

    def __str__(self):
        return f"{self.user.username} reacted with {self.reaction_type} to {self.post.title}"


class Comment(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)   #Concept: Self-referential relationship
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)   #Concept: Self-referential relationship
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    
    def __str__(self):
        return self.content[:30]

    def is_reply(self):
        return self.parent is not None

    def total_likes(self):
        return self.likes.count()