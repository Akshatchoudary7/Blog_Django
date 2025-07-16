from rest_framework import serializers
from .models import Post,Comment

class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    liked_users = serializers.SerializerMethodField() 
    like_count = serializers.SerializerMethodField()
    love_count = serializers.SerializerMethodField()
    funny_count = serializers.SerializerMethodField()
    angry_count = serializers.SerializerMethodField()
    loved_users = serializers.SerializerMethodField()
    funny_users = serializers.SerializerMethodField()
    angry_users = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'title', 'description', 'created_at', 'updated_at',
            'like_count', 'is_liked', 'dislike_count', 'is_disliked',
            'liked_users','love_count', 'funny_count', 'angry_count','loved_users', 'funny_users', 'angry_users'
        ]
        read_only_fields = ['user', 'like_count', 'dislike_count', 'is_liked', 'is_disliked',
                            'liked_users', 'loved_users', 'funny_users', 'angry_users']

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_dislike_count(self, obj):
        return obj.dislikes.count()
    
    
    def get_love_count(self, obj):
        return obj.loves.count()

    def get_funny_count(self, obj):
        return obj.funnies.count()

    def get_angry_count(self, obj):
        return obj.angries.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        return user and user.is_authenticated and obj.likes.filter(id=user.id).exists()

    def get_is_disliked(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        return user and user.is_authenticated and obj.dislikes.filter(id=user.id).exists()

    def get_liked_users(self, obj):
        return [user.username for user in obj.likes.all()]
    
    def get_loved_users(self, obj):
        return [user.username for user in obj.loves.all()]

    def get_funny_users(self, obj):
        return [user.username for user in obj.funnies.all()]

    def get_angry_users(self, obj):
        return [user.username for user in obj.angries.all()]    



class CommentSerializer(serializers.ModelSerializer):
    #post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    replies = serializers.SerializerMethodField()
    comment_content = serializers.PrimaryKeyRelatedField(
        source='parent',
        queryset=Comment.objects.all(),
        required=False,
        allow_null=True
    )
    post_title = serializers.CharField(source='post.title', read_only=True)


    class Meta:
        model = Comment
        fields = ['id', 'post','post_title', 'content', 'created_at', 'comment_content', 'replies']

    def get_replies(self, obj):
        return CommentSerializer(obj.replies.all(), many=True, context=self.context).data

    def validate(self, data):
        comment_content = data.get("parent")
        post = data.get("post")
        if comment_content and comment_content.post != post:
            raise serializers.ValidationError("Reply must be on the same post.")
        return data
    
