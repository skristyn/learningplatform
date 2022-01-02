from django.http import HttpRequest, JsonResponse
from django.urls import path
from .models import HomePage
from wagtail.api.v2.views import BaseAPIViewSet


class RootViewSet(BaseAPIViewSet):
    """
    This viewset should return the link to the users enrolled course, along with
    a link to their next incomplete section.
    """

    model = HomePage

    @classmethod
    def get_urlpatterns(cls):
        return [
            path("", cls.as_view({"get": "root_view"}), name="listing"),
        ]

    def root_view(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"data": "This is the data returned on the view"})
