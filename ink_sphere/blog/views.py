from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

def blog(request):
    context = {
        'posts': Post.objects.all()}
    return render(request, 'blog/blog.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})