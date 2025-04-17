from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='page-blog'),
    path('about/', views.about, name='page-about'),
]