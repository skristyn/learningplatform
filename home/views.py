from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from wagtail.api.v2.views import BaseAPIViewSet
from wagtail.api.v2.utils import get_object_detail_url
from materials.models import Textbook, Section, Lesson
from .models import HomePage, Announcement


def resolve_user_from_request(request):
    print("resolve_user_from_request ran")
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    print(auth_header)
    _, key = auth_header.split()
    token = Token.objects.get(key=key)
    print(token)
    return token.user


def api_login_required(view_func):
    """
    Wraps a view function to return an error message if a user accessing the API
    is not logged in.
    """
    def private_view_func(instance, request, *args, **kwargs):
        # First try to auth with token in header
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if auth_header:
            _, key = auth_header.split()
            try:
                token = Token.objects.get(key=key)
            except Token.DoesNotExist:
                return Response(
                    {"message": "The token provided isn't valid"}
                )
            request.user = token.user
            return view_func(instance, request, *args, **kwargs)
        if request.user.is_authenticated:
            return view_func(instance, request, *args, **kwargs)
        return Response(
            {"message": "Please log in to view any learning platform content"}
        )

    return private_view_func


class RootViewSet(BaseAPIViewSet):
    model = HomePage

    @classmethod
    def get_urlpatterns(cls):
        return [
            path("", cls.as_view({"get": "root_view"}), name="detail"),
        ]

    @api_login_required
    def root_view(self, request):
        hostname = request.build_absolute_uri()
        return Response(
            {
                "home": f"{hostname}home/",
                "courses": f"{hostname}textbooks/",
                "lessons": f"{hostname}lessons/",
                "sections": f"{hostname}sections/",
                "projects": f"{hostname}projects/",
                "resources": f"{hostname}resources/",
                "images": f"{hostname}images/",
                "url": f"{hostname}",
            }
        )


class HomeViewSet(BaseAPIViewSet):
    """
    These links aid in reaching the users current course and their next section.
    """

    model = HomePage

    @classmethod
    def get_urlpatterns(cls):
        return [
            path("", cls.as_view({"get": "home_view"}), name="detail"),
        ]

    @api_login_required
    def home_view(self, request):
        """
        : / Doing this so we're not returning a raw JsonResponse, but a drf one.
        Kinda a framework carcrash.
        """

        # if the user is not logged in, they'll have all kinds of errors.

        router = self.get_serializer_context()["router"]

        # The api_view decorator expects to wrap a simple function-based django views
        # not a wagtail APIViewset method...so wrapping an inner function. All knees
        # and elbows.

        @api_view(["GET"])
        def inner_view(request, *args, **kwargs):
            course = request.user.enrollment.active_course
            if course is not None:
                next_section = course.specific.next_section(request.user)
                next_lesson = next_section.get_parent()

                return Response(
                    {
                        "current_user": {
                            "username": request.user.username,
                            "id": request.user.id,
                        },
                        "current_course": {
                            "title": course.title,
                            "detail_url": get_object_detail_url(
                                router, request, Textbook, course.pk
                            ),
                        },
                        "current_lesson": {
                            "title": next_lesson.title,
                            "lesson_num": next_lesson.specific.number,
                            "detail_url": get_object_detail_url(
                                router, request, Lesson, next_lesson.pk
                            ),
                        },
                        "next_section": {
                            "title": next_section.title,
                            "section_num": next_section.specific.number,
                            "detail_url": get_object_detail_url(
                                router, request, Section, next_section.pk
                            ),
                        },
                        "announcement": Announcement.objects.latest("date").text,
                    }
                )

            return Response({
                "current_user": {
                    "username": request.user.username,
                    "id": request.user.id,
                },
            })

        return inner_view(request._request)

