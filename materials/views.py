import json
from django.http.response import JsonResponse
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import path
from django.contrib.auth.models import User
from wagtail.api.v2.views import BaseAPIViewSet
from .models import (
    Note,
    Textbook,
    Lesson,
    Grade,
    Section,
    Resource,
    ResourceAccess,
    Tip,
)
from home.views import api_login_required


class PrivateAPIViewSet(BaseAPIViewSet):
    """
    Subclass the base api viewset checking if the user is authenticated
    and returning a standard error response if not. There is probably a
    dryer way to do this.
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
    def get_urlpatterns(cls):
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
            path(
                "<int:pk>/", cls.as_view({"get": "detail_view"}), name="detail"
            ),
            path("find/", cls.as_view({"get": "find_view"}), name="find"),
        ]

    @api_login_required
    def create_grade(self, request: HttpRequest) -> JsonResponse:
        body = json.loads(request.body)
        student = get_object_or_404(User, pk=body["student"])
        section = get_object_or_404(Section, pk=body["section"])
        grade = Grade.objects.create(student=student, section=section)

        return JsonResponse(
            {
                "message": f"{section.title} was marked completed for {student.username}"
            }
        )


class TipViewSet(PrivateAPIViewSet):
    """
    Similar to the GradeViewSet a horrible hack that we all hate.
    """

    model = Tip

    @classmethod
    def get_urlpatterns(cls):
        """
        This can be empty for now.
        """
        return [
            path(
                "",
                cls.as_view({"get": "listing_view", "post": "create_tip"}),
                name="listing",
            ),
            path(
                "<int:pk>/", cls.as_view({"get": "detail_view"}), name="detail"
            ),
            path("find/", cls.as_view({"get": "find_view"}), name="find"),
        ]

    @api_login_required
    def listing_view(self, request):
        if (id := request.query_params.get("slide_id")) is not None:
            tips = Tip.objects.filter(slide_id=id).order_by("-created_at")
        else:
            tips = Tip.objects.all().order_by("-created_at")
        # tips -- will probably need to add paginations later.
        items = [
            {
                "user": tip.user.username,
                "body": tip.tip_body,
                "slide": tip.slide_id,
                "created_at": tip.created_at,
            }
            for tip in tips
        ]
        # would like to use drf Response object here, but getting an error.
        return JsonResponse(
            {"meta": {"total_count": len(items)}, "items": items}
        )

    @api_login_required
    def create_tip(self, request: HttpRequest) -> JsonResponse:
        body = json.loads(request.body)
        student = get_object_or_404(User, pk=body["student"])
        section = get_object_or_404(Section, pk=body["section"])
        Tip.objects.create(
            user=student,
            section=section,
            slide_id=body["slide_id"],
            tip_body=body["tip_body"],
        )

        return JsonResponse(
            {"message": f"{student.username} added tip successfully."}
        )


class NoteViewSet(PrivateAPIViewSet):
    """
    Similar to the GradeViewSet a horrible hack that we all hate.
    """

    model = Note

    @classmethod
    def get_urlpatterns(cls):
        """
        This can be empty for now.
        """
        return [
            path(
                "",
                cls.as_view({"get": "listing_view", "post": "create_notes"}),
                name="listing",
            ),
            path(
                "<int:pk>/", cls.as_view({"get": "detail_view"}), name="detail"
            ),
            path("find/", cls.as_view({"get": "find_view"}), name="find"),
        ]

    @api_login_required
    def listing_view(self, request):
        notes = Note.objects.filter(user=request.user)
        items = [
            {
                "username": note.user.username,
                "user_id": note.user.pk,
                "section": note.section.pk,
                "body": note.body,
                "created": note.created,
                "modified": note.modified,
            }
            for note in notes
        ]
        # would like to use drf Response object here, but getting an error.
        return JsonResponse(
            {"meta": {"total_count": len(items)}, "items": items}
        )

    @api_login_required
    def create_note(self, request: HttpRequest) -> JsonResponse:
        body = json.loads(request.body)
        student = get_object_or_404(User, pk=body["student"])
        section = get_object_or_404(Section, pk=body["section"])
        Note.objects.create(
            user=student,
            section=section,
            body=body["body"], # should this append on the back end?
        )

        return JsonResponse(
            {"message": f"{student.username} added note successfully."}
        )

    @api_login_required
    def update_note(self, request: HttpRequest, pk: int) -> JsonResponse:
        body = json.loads(request.body)
        student = request.user
        Note.objects.update_or_create(
            pk=pk,
            body=body["body"],
        )

        return JsonResponse({"message": f"{student} updated note successfully."})

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
