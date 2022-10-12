from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.urls import path
from .forms import ProfileUpdateForm
from django.contrib import messages
from .models import User
from django.views.generic import DetailView
from materials.views import PrivateAPIViewSet 
from home.views import api_login_required, Token


class UserApiViewSet(PrivateAPIViewSet):
    model = User

    @classmethod
    def get_urlpatterns(cls):
        """
        This can be empty for now.
        """
        return [
            path(
                "",
                cls.as_view({"get": "listing_view"}),
                name="listing",
            ),
        ]

    @api_login_required
    def listing_view(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        # If there is no auth, it will be caught by decorator

        _, key = auth_header.split()
        token = Token.objects.get(key=key)
        user = token.user
        user_obj = {
            "id": user.id,
            "pk": user.pk,
            "username": user.username,
            "pronouns": user.profile.pronouns,
            # "buddy": user.profile.buddy, # This needs to be linked up to a detail url
            "profile_complete": user.profile.user_completed, 
        }
        # would like to use drf Response object here, but getting an error.
        return JsonResponse(user_obj)


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
