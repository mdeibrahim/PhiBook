from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

class LikeUnlikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        reaction_type = request.data.get('reaction_type')

        if reaction_type not in ['like', 'unlike']:
            return Response({"error": "Invalid reaction type. Use 'like' or 'unlike'."}, status=400)

    
        Like.objects.update_or_create(
            post=post,
            user=request.user,
            defaults={'reaction_type': reaction_type}
        )

        return Response({
            "status": "success",
            "status_code": 200,
            "message": f"Post {reaction_type}d",
            "data":{
                "post_id": post.id,
                "user": request.user.email,
                "total_likes": post.total_likes,
                "total_unlikes": post.total_unlikes
            }
        })



class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            post_id = self.kwargs['pk']
            post = get_object_or_404(Post, pk=post_id)
            
            serializer.save(user=self.request.user, post=post)
            
            return Response({
                "status": "success",
                "status_code": 200,
                "message": "Comment added successfully",
                "data": serializer.data
            })
        return Response({
            "status": "error",
            "status_code": 400,
            "message": "Invalid data provided",
            "errors": serializer.errors
        }, status=400)


class ViewAllCommentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post).order_by('-created_at')  # Optional: latest first
        serializer = CommentSerializer(comments, many=True)
        return Response({
            "status": "success",
            "status_code": 200,
            "message": "Comments retrieved successfully",
            "data": serializer.data
        })


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can see all comments (for GET requests)
        return Comment.objects.all()

    def get_permissions(self):
        # For update/delete operations, check if user owns the comment
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def check_object_permissions(self, request, obj):
        # Allow GET for all authenticated users
        if request.method == 'GET':
            return super().check_object_permissions(request, obj)
        
        # For update/delete, only allow if user owns the comment
        if obj.user != request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only edit or delete your own comments.")
        
        return super().check_object_permissions(request, obj)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "status_code": 200,
            "message": "Comment retrieved successfully",
            "data": serializer.data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Check if user owns the comment
        if instance.user != request.user:
            return Response({
                "status": "error",
                "status_code": 403,
                "message": "You can only edit your own comments."
            }, status=403)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            "status": "success",
            "status_code": 200,
            "message": "Comment updated successfully",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check if user owns the comment
        if instance.user != request.user:
            return Response({
                "status": "error",
                "status_code": 403,
                "message": "You can only delete your own comments."
            }, status=403)
        
        self.perform_destroy(instance)
        return Response({
            "status": "success",
            "status_code": 200,
            "message": "Comment deleted successfully"
        })
