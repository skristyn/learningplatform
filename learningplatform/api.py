from django.urls import re_path, include
from wagtail.utils.urlpatterns import decorate_urlpatterns
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from home.views import RootViewSet
from materials.views import (
    LessonViewSet,
    SectionViewSet,
    GradeViewSet,
    SlideViewSet,
    TextbookViewSet,
)

# The wagtail api router is slightly different than the vanilla drf api router,
# so to deliver everything to the correct url we have to write ViewSets that
# are based on the wagtail BaseAPIViewSet, which is a little annoying because
# the documentation is lousy.


class RootableRouter(WagtailAPIRouter):
    """
    Need to subclass the router so it will allow you to call a view on the
    bare endpoint otherwise it has the annoying behavior of adding a second
    '/'.
    """

    @staticmethod
    def name_subdir(name: str) -> str:
        if name:
            return f"{name}/"
        return ""

    def get_urlpatterns(self):
        urlpatterns = [
            re_path(
                self.name_subdir(name),
                include((class_.get_urlpatterns(), name), namespace=name),
            )
            for name, class_ in self._endpoints.items()
        ]

        decorate_urlpatterns(urlpatterns, self.wrap_view)

        return urlpatterns


# Set the router instance
api_router = RootableRouter("learningplatformapi")

# register the endpoints.
api_router.register_endpoint("textbooks", TextbookViewSet)
api_router.register_endpoint("lessons", LessonViewSet)
api_router.register_endpoint("sections", SectionViewSet)
api_router.register_endpoint("slides", SlideViewSet)
api_router.register_endpoint("grades", GradeViewSet)
api_router.register_endpoint("images", ImagesAPIViewSet)
api_router.register_endpoint("", RootViewSet)
