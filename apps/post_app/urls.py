from django.urls import path
from .views import PostListCreateView, MyPostsView, LikeUnlikeView, CommentCreateView, CommentDetailView, ViewAllCommentsView

urlpatterns = [
    path('create-post/', PostListCreateView.as_view(), name='posts'), 
    path('my-posts/', MyPostsView.as_view(), name='my-posts'),
    path('view-all-posts/', MyPostsView.as_view(), name='view-all-posts'),

    path('posts/<int:pk>/like-unlike/', LikeUnlikeView.as_view(), name='like-unlike'),

    path('posts/<int:pk>/add-comment/', CommentCreateView.as_view(), name='add-comment'),
    path('posts/<int:pk>/view-all-comments/', ViewAllCommentsView.as_view(), name='view-all-comments'),

    path('edit-comment/<int:pk>/', CommentDetailView.as_view(), name='edit-comment'),
    path('delete-comment/<int:pk>/', CommentDetailView.as_view(), name='delete-comment'),
    path('update-comment/<int:pk>/', CommentDetailView.as_view(), name='update-comment'),
]
