from .models import Post,Comment
from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    reaction_counts = serializers.SerializerMethodField()
    user_reaction = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'description', 'created_at', 'updated_at', 'reaction_counts', 'user_reaction']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'user_reaction']

    def get_reaction_counts(self, obj):
        reactions = obj.reactions.values('reaction_type').annotate(count=models.Count('id'))
        return {r['reaction_type']: r['count'] for r in reactions}

    def get_user_reaction(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return None
        reaction = obj.reactions.filter(user=user).first()
        return reaction.reaction_type if reaction else None

        return [{'id': user.id, 'username': user.username} for user in reacted_users]
class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    comment_content = serializers.PrimaryKeyRelatedField(source='parent', queryset=Comment.objects.all(), required=False, allow_null=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    post_title = serializers.SerializerMethodField()  

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'post_title', 'content', 'created_at',
            'comment_content', 'like_count', 'is_liked', 'replies'
        ]

    def get_post_title(self, obj):
        return obj.post.title if obj.post else None

    def get_replies(self, obj):
        replies = obj.replies.filter(post=obj.post)
        return CommentSerializer(replies, many=True, context=self.context).data

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False

    def validate(self, data):
        comment_content = data.get("comment_content")
        post = data.get("post")
        if comment_content and comment_content.post != post:
            raise serializers.ValidationError("comment_content comment must be on the same post.")
        return data

    
