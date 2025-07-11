from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post,Comment
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
    
    def get_serializer_context(self):
        return {'request': self.request}  # for `is_liked`

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        post.likes.add(request.user)
        return Response({'status': 'post liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        post.likes.remove(request.user)
        return Response({'status': 'post unliked'}, status=status.HTTP_200_OK)
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.request.GET.get('post')
        if post_id:
            return Comment.objects.filter(post_id=post_id, parent__isnull=True)
        return Comment.objects.filter(parent__isnull=True)