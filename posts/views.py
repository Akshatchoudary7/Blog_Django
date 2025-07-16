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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] #Anyone can read; only logged-in users can write
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
    pagination_class = PostCursorPagination
    

    def get_serializer_context(self): #Passes the request object to the serializer so it can access the user (needed for is_liked)
        return {'request': self.request}

    def perform_create(self, serializer): #ensures the post is always saved with the current logged-in user
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def react(self, request, pk=None):
        post = self.get_object()
        user = request.user
        reaction_type = request.data.get('type')  # like, love, funny, angry

    # First remove user from all reactions
        post.likes.remove(user)
        post.loves.remove(user)
        post.funnies.remove(user)
        post.angries.remove(user)

    # Add user to selected reaction
        if reaction_type == 'like':
            post.likes.add(user)
        elif reaction_type == 'love':
            post.loves.add(user)
        elif reaction_type == 'funny':
            post.funnies.add(user)
        elif reaction_type == 'angry':
            post.angries.add(user)
        else:
            return Response({"detail": "Invalid reaction type."}, status=400)

        return Response({
            "reaction": reaction_type,
            "like_count": post.likes.count(),
            "love_count": post.loves.count(),
            "funny_count": post.funnies.count(),
            "angry_count": post.angries.count()
        })

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
    #If you pass ?post=3, it filters comments for post ID 3.
    def get_queryset(self):
        post_id = self.request.GET.get('post') 
        if post_id: 
            return Comment.objects.filter(post_id=post_id, parent__isnull=True) 
        return Comment.objects.filter(parent__isnull=True) 
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

