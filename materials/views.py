from typing import List, Callable
from django.http.response import JsonResponse
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import path
from django.contrib.auth.models import User
from wagtail.api.v2.views import BaseAPIViewSet
from .models import Textbook, Lesson, Grade, Section, Resource, ResourceAccess, Tip
from home.views import api_login_required


class PrivateAPIViewSet(BaseAPIViewSet):
    """
    Subclass the base api viewset checking if the user is authenticated and
    returning a standard error response if not. There is probably a dryer way
    to do this.
    """

    @api_login_required
    def listing_view(self, *args, **kwargs):
        return super().listing_view(*args, **kwargs)

    @api_login_required
    def detail_view(self, *args, **kwargs):
        return super().detail_view(*args, **kwargs)

    @api_login_required
    def find_view(self, *args, **kwargs):
        return super().find_view(*args, **kwargs)


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

    @api_login_required
    def create_grade(self, request: HttpRequest) -> JsonResponse:
        student = get_object_or_404(User, pk=request.POST["student"])
        section = get_object_or_404(Section, pk=request.POST["section"])
        Grade.objects.create(student=student, section=section)

        return JsonResponse(
            {"message": f"{section.title} was marked completed for {student.username}"}
        )


class TipViewSet(PrivateAPIViewSet):
    """
    Similar to the GradeViewSet a horrible hack that we all hate.
    """
    model = Tip
    
    @classmethod
    def get_urlpatterns(cls) -> List[Callable]:
        """
        This can be empty for now.
        """
        return [
            path(
                "",
                cls.as_view({"get": "listing_view", "post": "create_tip"}),
                name="listing",
            ),
            path("<int:pk>/", cls.as_view({"get": "detail_view"}), name="detail"),
            path("find/", cls.as_view({"get": "find_view"}), name="find"),
        ]

    @api_login_required
    def listing_view(self, request) -> str:
        if (id := request.query_params.get('slide_id')) is not None:
            tips = Tip.objects.filter(slide_id=id)
        else:
            tips = Tip.objects.all()
        # tips -- will probably need to add paginations later.
        items = [
            {
                "user": tip.user.username,
                "body": tip.tip_body,
                "slide": tip.slide_id,
            } for tip in tips
        ]
        # would like to use drf Response object here, but getting an error.
        return JsonResponse(
            {
                "meta": {
                    "total_count": len(items)
                },
                "items": items
            }
        )

    @api_login_required
    def create_tip(self, request: HttpRequest) -> JsonResponse:
        student = get_object_or_404(User, pk=request.POST["student"])
        section = get_object_or_404(Section, pk=request.POST["section"])
        slide = request.POST["slide"]
        Tip.objects.create(user=student, section=section)

        return JsonResponse(
            {"message": f"{student.username} added tip successfully."}
        )


# The wagtail BaseAPIViewSet provides listing and detail views when provided
# a model.


class TextbookViewSet(PrivateAPIViewSet):
    """
    The textbook is the root of the course content tree. Its children are lessons.
    """

    model = Textbook


class LessonViewSet(PrivateAPIViewSet):
    """
    Lessons are the broadest subdivision of the course content. They are analagous
    to a chapter in a book.
    """

    model = Lesson


class SectionViewSet(PrivateAPIViewSet):
    """
    Sections are the subdivision of the course material that a user will work through
    in one sitting ideally. They are the unit that the student can mark completed, though
    this is done with an appropriate POST request to the .../grades/ endpoint.
    """

    model = Section


class ResourceViewSet(PrivateAPIViewSet):
    model = Resource

    def detail_view(self, request, *args, **kwargs):
        resource = self.get_object()
        ResourceAccess.objects.create(resource=resource, student=request.user)
        return super().detail_view(request, *args, **kwargs)
