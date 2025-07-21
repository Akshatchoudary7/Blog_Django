from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment,Reaction
from .pagination import PostCursorPagination
from django.db import transaction
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] #Anyone can read; only logged-in users can write
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
    pagination_class = PostCursorPagination
    

    def get_serializer_context(self): #Passes the request object to the serializer so it can access the user (needed for is_liked)
        return {'request': self.request}

    def perform_create(self, serializer): #ensures the post is always saved with the current logged-in user
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    @transaction.atomic
    def react(self, request, pk=None):
        post = self.get_object()
        user = request.user
        reaction_type = request.data.get('type')

        if reaction_type not in dict(Reaction.ReactionType.choices):
            return Response({'detail': 'Invalid reaction type.'}, status=status.HTTP_400_BAD_REQUEST)

        Reaction.objects.update_or_create(
            user=user,
            post=post,
            defaults={'reaction_type': reaction_type}
        )

        return Response({'status': 'success', 'reaction': reaction_type})

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def reactions(self, request, pk=None):
        post = self.get_object()
        counts = Reaction.objects.filter(post=post).values('reaction_type').annotate(count=Count('id'))
        return Response({c['reaction_type']: c['count'] for c in counts})

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