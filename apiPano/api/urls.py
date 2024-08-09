# urls.py
from django.urls import path
from apiPano.api.views import viewPosts, viewPost, get_user, addPost, updatePost, deletePost,login,search_posts
urlpatterns = [
    path('api/login/', login, name='login'),
    path('api/viewposts/', viewPosts, name='view-posts'),
    path('api/post/<int:pk>/', viewPost, name='view-post'),
    path('api/post/add/', addPost, name='add-post'),
    path('api/post/update/<int:pk>/', updatePost, name='update-post'),
    path('api/post/delete/<int:pk>/', deletePost, name='delete-post'),
    path('api/user/', get_user, name='get_user'),
    path('api/posts/search/', search_posts, name='search_posts'),
]
