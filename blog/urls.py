from django.urls import path

from . import views
from .views import (
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    UserPostListView,
    PostUpdateView,
    SubscribeView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="page-blog"),
    path("user/<int:pk>", UserPostListView.as_view(), name="post-user-list"),
    path("detail/<int:pk>", PostDetailView.as_view(), name="post-detail"),
    path("update/<int:pk>", PostUpdateView.as_view(), name="post-update"),
    path("delete/<int:pk>", PostDeleteView.as_view(), name="post-delete"),
    path("create/", PostCreateView.as_view(), name="post-create"),
    path("<int:pk>", SubscribeView.as_view(), name="subscribe"),
    path("about/", views.about, name="page-about"),
]
