from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm


class CustomPasswordResetView(PasswordResetView):
    template_name = "user/reset_password.html"
    html_email_template_name = "user/password_reset_email.html"
    subject_template_name = "user/password_reset_subject.txt"


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account created for {username}! You can now log in."
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "user/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get("username")
            messages.success(request, f"Profile updated for {username}!")
            return redirect("page-blog")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {"u_form": u_form, "p_form": p_form}
    return render(request, "user/profile.html", context)
