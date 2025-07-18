from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    reaction_counts = serializers.SerializerMethodField()
    user_reaction = serializers.SerializerMethodField()
    reacted_users = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'description', 'created_at', 'updated_at',
                  'reaction_counts', 'user_reaction', 'reacted_users']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'user_reaction']

    def get_reaction_counts(self, obj):
        return {
            'like': obj.like_count,
            'dislike': obj.dislike_count,
            'love': obj.love_count,
            'funny': obj.funny_count,
            'sad': obj.sad_count,
            'shock': obj.shock_count
        }

    def get_user_reaction(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            return obj.reactions_data.get(str(user.id))
        return None

    def get_reacted_users(self, obj):
        user_ids = obj.reactions_data.keys()
        users = User.objects.filter(id__in=user_ids)
        return [user.username for user in users]


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    parent_id = serializers.PrimaryKeyRelatedField(
        source='parent', queryset=Comment.objects.all(), required=False, allow_null=True
    )
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    post_title = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'post_title', 'content', 'created_at',
            'parent_id', 'like_count', 'is_liked', 'replies'
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
        parent = data.get("parent")
        post = data.get("post")
        if parent and parent.post_id != post.id:
            raise serializers.ValidationError("A reply must be on the same post as its parent comment.")
        return data
