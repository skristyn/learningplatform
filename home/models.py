from django.db import models
from django.urls import reverse
from django.http import HttpResponseRedirect

from wagtail.core.models import Page


def wagtail_require_login(serve):
    """
    To guarentee the user is authenticated before seeing this page, you can
    wrap the serve function with this.
    """

    def wrapped_serve(self, request, *args, **kwargs):
        """
        If the user is not logged in return a redirect response object pointed at
        the login url otherwise return the template response object as usual.
        """
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("users:login"))
        return serve(self, request, *args, **kwargs)

    return wrapped_serve


class HomePage(Page):
    """
    This is the landing page of the site.
    """

    max_count = 1

    def get_context(self, request):
        context = super().get_context(request)
        return context

    @wagtail_require_login
    def serve(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)
