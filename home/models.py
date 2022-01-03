from typing import Callable
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from rest_framework.serializers import Field
from wagtail.core.models import Page
from wagtail.api import APIField


class HomePage(Page):
    """
    This is the landing page of the site.
    """

    max_count = 1
