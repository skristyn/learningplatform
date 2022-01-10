from typing import Callable
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from rest_framework.serializers import Field
from wagtail.core.models import Page
from wagtail.api import APIField


class Announcement(models.Model):
    """
    A short message broadcast to students on the homepage.
    """
    date = models.DateField(auto_now_add=True)
    text = models.TextField()


class HomePage(Page):
    """
    Landing page of the site.
    """

    max_count = 1

    def get_context(self, request):
        context: dict = super().get_context(request)
        context['announcement'] = Announcement.objects.get_latest('date')

