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
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if post.likes.filter(id=user.id).exists():
            return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        
        post.dislikes.remove(user)

        post.likes.add(user)
        return Response({
            'status': 'liked',
            'like_count': post.likes.count(),
            'dislike_count': post.dislikes.count(),
            'is_liked': True,
            'is_disliked': False
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def dislike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if post.dislikes.filter(id=user.id).exists():
            return Response({'detail': 'You have already disliked this post.'}, status=status.HTTP_400_BAD_REQUEST)

     
        post.likes.remove(user)

        post.dislikes.add(user)
        return Response({
            'status': 'disliked',
            'dislike_count': post.dislikes.count(),
            'like_count': post.likes.count(),
            'is_disliked': True,
            'is_liked': False
        }, status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer 
    pagination_class = None

    def get_queryset(self):
        post_id = self.request.GET.get('post') 
        if post_id: 
            return Comment.objects.filter(post_id=post_id, parent__isnull=True) 
        return Comment.objects.filter(parent__isnull=True) 
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

