from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def blog(request):
    context = {
        'posts': Post.objects.all()}
    return render(request, 'blog/blog.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  
    ordering = ['-date_posted']
    # context_object_name = 'posts'
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content'] 
    template_name = 'blog/post_update.html'

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author

    def get_success_url(self):
        return reverse('page-blog')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content'] 
    template_name = 'blog/post_update.html'

    def get_success_url(self):
        return reverse('page-blog')

def about(request):
    print(reverse('page-detail', kwargs={'pk': 1}))
    return render(request, 'blog/about.html', {'title': 'About'})