from rest_framework import serializers
from .models import Post,Comment

class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj.likes.filter(id=user.id).exists()

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    
    
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(),required=False,allow_null=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'created_at', 'parent', 'replies']

    def get_replies(self, obj):
        return CommentSerializer(obj.replies.all(), many=True, context=self.context).data
    
    
    
    def validate(self, data):
      
        parent = data.get("parent")
        post = data.get("post")
        if parent and parent.post != post:
            raise serializers.ValidationError("parent comment must be on the same post.")
        return data

    
