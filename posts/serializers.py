from rest_framework import serializers
from .models import Post,Comment

class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'title', 'description', 'created_at', 'updated_at',
            'like_count', 'is_liked', 'dislike_count', 'is_disliked'
        ]
        read_only_fields = ['user', 'like_count', 'dislike_count', 'is_liked', 'is_disliked']

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_dislike_count(self, obj):
        return obj.dislikes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        return user and user.is_authenticated and obj.likes.filter(id=user.id).exists()

    def get_is_disliked(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        return user and user.is_authenticated and obj.dislikes.filter(id=user.id).exists()


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    
    
    comment_content = serializers.PrimaryKeyRelatedField(source='parent', queryset=Comment.objects.all(), required=False,
    allow_null=True
)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'created_at', 'comment_content', 'replies']
        

    def get_replies(self, obj):
        return CommentSerializer(obj.replies.all(), many=True, context=self.context).data
    
    
    
    def validate(self, data):
      
        comment_content = data.get("comment_content")
        post = data.get("post")
        if comment_content and comment_content.post != post:
            raise serializers.ValidationError("comment_content comment must be on the same post.")
        return data

    
