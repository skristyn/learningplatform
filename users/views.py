from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileUpdateForm
from django.contrib import messages
from .models import User
from django.views.generic import DetailView


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User


@login_required
def update_profile(request):
    if request.method == "POST":
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user
        )
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("users:detail", request.user.pk)

    else:
        profile_form = ProfileUpdateForm(instance=request.user)

    return render(request, "users/update_profile.html", {"profile_form": profile_form})


@login_required
def community(request):
    buddies = request.user.buddy.all()
    announcement = ""
    context = {"buddies": buddies, "announcement": announcement}
    return render(request, "users/community.html", context)
