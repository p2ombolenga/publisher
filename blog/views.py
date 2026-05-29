from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.text import slugify
from .models import Post, Comment, Tag
from .serializers import *
from .permissions import IsAuthorOrReadOnly

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status='published').order_by('-created_at')
    serializer_class = PostSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated()] if self.request.method == 'POST' else [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, slug=slugify(serializer.validated_data['title']))

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        post.views += 1
        post.save()
        return Response(PostSerializer(post).data)
    
class MyPostView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_at')
    
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'], is_approved=True)
    
    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(post_id=self.kwargs['post_id'], author=user)

class CommentApproveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        if comment.post.author != request.user:
            return Response({'Error': 'Not Allowed'}, status=403)
        comment.is_approved = True
        comment.save()
        return Response({'status': 'Status Approved'})
    
class TagListView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer = TagSerializer