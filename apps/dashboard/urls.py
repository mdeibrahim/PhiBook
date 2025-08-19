from django.urls import path
from .views import CreatePostView, UpdatePostView,DeletePostView, LikeUnlikeView,ViewMyPostsView,ViewAllPostsView,AddCommentView,UpdateCommentView,DeleteCommentView,ViewAllCommentsView

urlpatterns = [
    path('create-post/', CreatePostView.as_view(), name='create-post'), 
    path('update-post/<int:pk>/', UpdatePostView.as_view(), name='update-post'), 
    path('delete-post/<int:pk>/', DeletePostView.as_view(), name='delete-post'), 

    path('view-my-posts/', ViewMyPostsView.as_view(), name='view-my-posts'),
    path('view-all-posts/', ViewAllPostsView.as_view(), name='view-all-posts'),

    path('posts/<int:pk>/like-unlike/', LikeUnlikeView.as_view(), name='like-unlike'),

    path('add-comment/<int:pk>/', AddCommentView.as_view(), name='add-comment'),
    path('update-comment/<int:post_pk>/<int:pk>/', UpdateCommentView.as_view(), name='update-comment'),
    path('delete-comment/<int:post_pk>/<int:pk>/', DeleteCommentView.as_view(), name='delete-comment'),
    
    path('view-all-comments/<int:pk>/', ViewAllCommentsView.as_view(), name='view-all-comments'),
]
