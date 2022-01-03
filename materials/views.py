from typing import List, Callable
from django.http.response import JsonResponse
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.urls import path
from django.contrib.auth.models import User
from wagtail.api.v2.views import BaseAPIViewSet
from .models import Textbook, Lesson, Section, Slide, Grade


class GradeViewSet(BaseAPIViewSet):
    """
    While the other viewsets provide the pages/tree like expected, this viewset
    must be customized to accept POST requests notifying the system about a user
    completing a section.
    """

    model = Grade

    @classmethod
    def get_urlpatterns(cls) -> List[Callable]:
        """
        Returns a list of URL patterns for the endpoint. Each http method
        can be provided its own view method within the dictionaries provided to
        the as_view method call.
        """
        return [
            path(
                "",
                cls.as_view({"get": "listing_view", "post": "create_grade"}),
                name="listing",
            ),
            path("<int:pk>/", cls.as_view({"get": "detail_view"}), name="detail"),
            path("find/", cls.as_view({"get": "find_view"}), name="find"),
        ]

    def create_grade(self, request: HttpRequest) -> JsonResponse:
        student = get_object_or_404(User, pk=request.POST["student"])
        section = get_object_or_404(Section, pk=request.POST["section"])
        Grade.objects.create(student=student, section=section)

        return JsonResponse(
            {"message": f"{section.title} was marked completed for {student.username}"}
        )


# The wagtail BaseAPIViewSet provides listing and detail views when provided
# a model.


class TextbookViewSet(BaseAPIViewSet):
    """
    The textbook is the root of the course content tree. Its children are lessons.
    """

    model = Textbook


class LessonViewSet(BaseAPIViewSet):
    """
    Lessons are the broadest subdivision of the course content. They are analagous
    to a chapter in a book.
    """

    model = Lesson


class SectionViewSet(BaseAPIViewSet):
    """
    Sections are the subdivision of the course material that a user will work through
    in one sitting ideally. They are the unit that the student can mark completed, though
    this is done with an appropriate POST request to the .../grades/ endpoint.
    """

    model = Section


class SlideViewSet(BaseAPIViewSet):
    """
    Slides are where the bulk of the content is grouped. The course author will spend
    most of the time developing on the slides.
    """

    model = Slide
