from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
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
from newsletter_generator.shemas.enums import SubscriptionType
from user.models import Profile


def blog(request):
    context = {"posts": Post.objects.all()}
    return render(request, "blog/blog.html", context)


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    ordering = ["-date_posted"]
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts_list.html"
    paginate_by = 5

    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs["pk"])
        return Post.objects.filter(author=user).order_by("-date_posted")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = User.objects.get(pk=self.kwargs['pk'])
        return context
       
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

from django.shortcuts import redirect, get_object_or_404
from django.views import View
# def subscribe(request, pk):
#     if request.method == "POST":
#         action = request.POST.get("action")
#         subscriber = request.user
#         user = User.objects.get(pk=pk)
#         profile = Profile.objects.filter(user=user).first()
#         if action == SubscriptionType.subscribe:
#             print("the subscriber doesn't exist")
#             if profile and subscriber not in profile.subscribers.all():
#                 profile.subscribers.add(subscriber)
#         else:
#             print("the subscriber exists")
#             print(profile.subscribers.all())
#             if profile and subscriber in profile.subscribers.all():
#                 profile.subscribers.remove(subscriber)

#         return redirect("post-user-list", pk=pk)

class SubscribeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        action = request.POST.get("action")
        subscriber = request.user
        user = get_object_or_404(User, pk=pk)
        profile = Profile.objects.filter(user=user).first()

        if action == SubscriptionType.subscribe:
            if profile and subscriber not in profile.subscribers.all():
                profile.subscribers.add(subscriber)
        else:
            if profile and subscriber in profile.subscribers.all():
                profile.subscribers.remove(subscriber)

        return redirect("post-user-list", pk=pk)


    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(subscribers=user)

def about(request):
    return render(request, "blog/about.html", {"title": "About"})
