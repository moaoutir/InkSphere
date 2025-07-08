from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Post


def blog(request):
    context = {"posts": Post.objects.all()}
    return render(request, "blog/blog.html", context)


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    ordering = ["-date_posted"]
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]
    template_name = "blog/post_update.html"

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_delete.html"

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author

    def get_success_url(self):
        return reverse("page-blog")


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]
    template_name = "blog/post_update.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("page-blog")


def about(request):
    return render(request, "blog/about.html", {"title": "About"})
