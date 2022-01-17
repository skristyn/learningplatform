from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from wagtail.api.v2.views import BaseAPIViewSet
from wagtail.api.v2.utils import get_object_detail_url
from materials.models import Textbook, Section
from .models import HomePage, Announcement


def api_login_required(view_func):
    """
    Wraps a view function to return an error message if a user accessing the API
    is not logged in.
    """
    def private_view_func(instance, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"message": "Please log in to view any learning platform content"}
            )
        return view_func(instance, request, *args, **kwargs)
    return private_view_func


class RootViewSet(BaseAPIViewSet):
    """
    These links aid in reaching the users current course and their next section.
    """

    model = HomePage

    @classmethod
    def get_urlpatterns(cls):
        return [
            path("", cls.as_view({"get": "root_view"}), name="detail"),
        ]

    @api_login_required
    def root_view(self, request):
        """
        : / Doing this so we're not returning a raw JsonResponse, but a drf one.
        Kinda a framework carcrash.
        """

        # if the user is not logged in, they'll have all kinds of errors.

        router = self.get_serializer_context()["router"]
        course = request.user.enrollment.active_course
        next_section = course.specific.next_section(request.user)
        print(next_section)

        # The api_view decorator expects to wrap a simple function-based django views
        # not a wagtail APIViewset method...so wrapping an inner function. All knees
        # and elbows.

        @api_view(["GET"])
        def inner_view(request, *args, **kwargs):

            return Response(
                {
                    "current_course": {
                        "title": course.title,
                        "detail_url": get_object_detail_url(
                            router, request, Textbook, course.pk
                        ),
                    },
                    "next_section": {
                        "title": next_section.title,
                        "detail_url": get_object_detail_url(
                            router, request, Section, next_section.pk
                        ),
                    },
                "announcement": Announcement.objects.latest('date').text,
                }
            )

        # The view cannot be called with a drf request object, but the underlying
        # django request object accessed by the _request attribute.
        return inner_view(request._request)
