from django.urls import path
from .views import PostListCreateView, MyPostsView, LikeUnlikeView, CommentCreateView, CommentDetailView, ViewAllCommentsView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='posts'),
    path('my-posts/', MyPostsView.as_view(), name='my-posts'),
    path('posts/<int:pk>/like-unlike/', LikeUnlikeView.as_view(), name='like-unlike'),
    path('posts/<int:pk>/comment/', CommentCreateView.as_view(), name='add-comment'),
    path('posts/<int:pk>/view-all-comments/', ViewAllCommentsView.as_view(), name='view-all-comments'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
