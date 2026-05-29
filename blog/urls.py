from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view()),
    path('posts/', views.PostListCreateView.as_view()),
    path('posts/mine/', views.MyPostView.as_view()),
    path('posts/<slug:slug>/', views.PostDetailView.as_view()),
    path('posts/<int:post_id>/comments/', views.CommentListCreateView.as_view()),
    path('comments/<int:pk>/approve/', views.CommentApproveView.as_view()),
    path('tags/', views.TagListView.as_view()),
]