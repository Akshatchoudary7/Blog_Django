from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):     
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    title = models.CharField(max_length=255)
    description = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True)
    loves = models.ManyToManyField(User, related_name='loved_posts', blank=True)
    funnies = models.ManyToManyField(User, related_name='funny_posts', blank=True)
    angries = models.ManyToManyField(User, related_name='angry_posts', blank=True)


    def __str__(self):  
        return self.title 

    def total_likes(self):  #Returns how many users have liked the post.
        return self.likes.count()
    
    def total_dislikes(self):
        return self.dislikes.count()
    
    def total_loves(self):
        return self.loves.count()

    def total_funnies(self):
        return self.funnies.count()

    def total_angries(self):
        return self.angries.count()

class Comment(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)   #Concept: Self-referential relationship
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)   #Concept: Self-referential relationship

    def __str__(self):
        return self.content[:30]

    def is_reply(self):
        return self.parent is not None

