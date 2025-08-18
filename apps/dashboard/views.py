from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer


class CreatePostView(APIView):
    """
    Create a new post with text, image, or video.
    
    **Authentication:** Required
    **Request Body:** text (required), image (optional), video_url (optional)
    **Response:** Created post data or validation errors
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "status": "success",
                "status_code": 200,
                "message": "Post created successfully",
                "data": serializer.data
            }, status=200)
        return Response({
            "status": "error",
            "status_code": 400,
            "message": "Invalid data provided",
            "errors": serializer.errors
        }, status=400)
    

class UpdatePostView(APIView):
    """
    Update an existing post (owner only).
    
    **Authentication:** Required
    **URL Parameters:** pk (post ID)
    **Request Body:** text, image, or video_url (all optional)
    **Response:** Updated post data or errors
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.serializer_class(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "status_code": 200,
                "message": "Post updated successfully",
                "data": serializer.data
            }, status=200)
        return Response({
            "status": "error",
            "status_code": 400,
            "message": "Invalid data provided",
            "errors": serializer.errors
        }, status=400)
    
class DeletePostView(APIView):
    """
    Delete a post (owner only).
    
    **Authentication:** Required
    **URL Parameters:** pk (post ID)
    **Response:** Success message or authorization error
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.user != request.user:
            return Response({
                "status": "error",
                "status_code": 403,
                "message": "You can only delete your own posts."
            }, status=403)
        post.delete()
        return Response({
            "status": "success",
            "status_code": 200,
            "message": "Post deleted successfully"
        }, status=200)
    


class ViewMyPostsView(APIView):
    """
    Retrieve current user's posts.
    
    **Authentication:** Required
    **Response:** List of user's posts or 404 if none found
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        posts = Post.objects.filter(user=request.user)
        if not posts:
            return Response({
                "status": "error",
                "status_code": 404,
                "message": "No posts found"
            }, status=404)
        serializer = self.serializer_class(posts, many=True)
        return Response({
            "status": "success",
            "status_code": 200,
            "message": "Posts retrieved successfully",
            "data": serializer.data
        }, status=200)
    

class ViewAllPostsView(APIView):
    """
    Retrieve all posts from all users.
    
    **Authentication:** Required
    **Response:** List of all posts
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = self.serializer_class(posts, many=True)
        return Response({
            "status": "success",
            "status_code": 200,
            "message": "Posts retrieved successfully",
            "data": serializer.data
        }, status=200)
    
    
class ViewAllPostsView(APIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        posts = Post.objects.all()
        if not posts:
            return Response({
                "status": "error",
                "status_code": 404,
                "message": "No posts found"
            }, status=404)
        serializer = self.serializer_class(posts, many=True)
        return Response({
            "status": "success",
            "status_code": 200,
            "message": "Posts retrieved successfully",
            "data": serializer.data
        }, status=200)


class LikeUnlikeView(APIView):
    """
    Like or unlike a post.
    
    **Authentication:** Required
    **Request Body:** reaction_type (string): 'like' or 'unlike'
    **Response:** Success message with updated like counts
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        reaction_type = request.data.get('reaction_type')

        if reaction_type not in ['like', 'unlike']:
            return Response({
                "status": "error",
                "status_code": 400,
                "message": "Invalid reaction type. Use 'like' or 'unlike'."
            }, status=400)
    
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



class AddCommentView(APIView):
    """
    Add a comment to a post.
    
    **Authentication:** Required
    **Request Body:** comment (string): Comment text
    **Response:** Created comment data
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            post_id = self.kwargs['pk']
            post = get_object_or_404(Post, pk=post_id)
            
            serializer.save(user=request.user, post=post)
            
            return Response({
                "status": "success",
                "status_code": 200,
                "message": "Comment added successfully",
                "data": serializer.data
            }, status=200)
        return Response({
            "status": "error",
            "status_code": 400,
            "message": "Invalid data provided",
            "errors": serializer.errors
        }, status=400)
    

class UpdateCommentView(APIView):
    """
    Update a comment.
    
    **Authentication:** Required
    **Request Body:** comment (string): Updated comment text
    **Response:** Updated comment data
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = self.serializer_class(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
            "status": "success",
            "status_code": 200,
            "message": "Comment updated successfully",
            "data": serializer.data
        }, status=200)
        return Response({
            "status": "error",
            "status_code": 400,
            "message": "Invalid data provided",
            "errors": serializer.errors
        }, status=400)
    
class DeleteCommentView(APIView):
    """
    Delete a comment.
    
    **Authentication:** Required
    **Response:** Success message
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response({
            "status": "success",
            "status_code": 200,
            "message": "Comment deleted successfully"
        }, status=200)
    

class ViewAllCommentsView(APIView):
    """
    Retrieve all comments for a specific post.
    
    **Authentication:** Required
    **Response:** List of comments ordered by creation date
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response({
            "status": "success",
            "status_code": 200,
            "message": "Comments retrieved successfully",
            "data": serializer.data
        }, status=200)

