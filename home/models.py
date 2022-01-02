from typing import Callable
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from wagtail.core.models import Page
from wagtail.api import APIField


class HomePage(Page):
    """
    This is the landing page of the site.
    """

    max_count = 1

    def next_incomplete_section(self, student: User):
        pass

    def course_overview(self, student: User):
        course = student.enrollment.active_course

    def get_context(self, request: HttpRequest) -> dict:
        context: dict = super().get_context(request)
        return context

