from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment
from rest_framework.authtoken.models import Token
from .pagination import PostCursorPagination
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
    pagination_class = PostCursorPagination

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def react(self, request, pk=None):
        post = self.get_object()
        user = request.user
        user_id_str = str(user.id)
        new_reaction = request.data.get('type')

        valid_reactions = ['like', 'dislike', 'love', 'funny', 'sad', 'shock']
        if new_reaction not in valid_reactions:
            return Response({'detail': 'Invalid reaction type'}, status=400)

        old_reaction = post.reactions_data.get(user_id_str)

        if old_reaction and old_reaction in valid_reactions:
            old_count = getattr(post, f"{old_reaction}_count")
            setattr(post, f"{old_reaction}_count", max(0, old_count - 1))

        if old_reaction == new_reaction:
            post.reactions_data.pop(user_id_str, None)
            post.save()
            return Response({
                "status": "reaction removed",
                "reaction": None,
                "counts": self.get_reaction_counts(post)
            })

        setattr(post, f"{new_reaction}_count", getattr(post, f"{new_reaction}_count") + 1)
        post.reactions_data[user_id_str] = new_reaction
        post.save()

        return Response({
            "status": "reaction updated",
            "reaction": new_reaction,
            "counts": self.get_reaction_counts(post)
        })

    def get_reaction_counts(self, post):
        return {
            'like': post.like_count,
            'dislike': post.dislike_count,
            'love': post.love_count,
            'funny': post.funny_count,
            'sad': post.sad_count,
            'shock': post.shock_count
        }


   


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer 
    pagination_class = None 
   
    #If you pass ?post=3, it filters comments for post ID 3.
    def get_queryset(self):
        post_id = self.request.GET.get('post') 
        if post_id: 
            return Comment.objects.filter(post_id=post_id, parent__isnull=True) 
        return Comment.objects.filter(parent__isnull=True) 
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def toggle_like(self, request, pk=None):
        comment = self.get_object()
        user = request.user

        if comment.likes.filter(id=user.id).exists():
            comment.likes.remove(user)
            return Response({
            'status': 'unliked',
            'like_count': comment.likes.count(),
            'is_liked': False
            })
        else:
            comment.likes.add(user)
            return Response({
                'status': 'liked',
                'like_count': comment.likes.count(),
                'is_liked': True
            })
