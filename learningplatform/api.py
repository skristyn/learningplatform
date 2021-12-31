from wagtail.api.v2.router import WagtailAPIRouter
from materials.views import LessonViewSet, SectionViewSet, GradeViewSet, SlideViewSet

# The wagtail api router is slightly different than the vanilla drf api router,
# so to deliver everything to the correct url we have to write ViewSets that
# are based on the wagtail BaseAPIViewSet, which is a little annoying because
# the documentation is lousy.

# Set the router instance
api_router = WagtailAPIRouter('learningplatformapi')

# register the endpoints.
api_router.register_endpoint('lessons', LessonViewSet)
api_router.register_endpoint('sections', SectionViewSet)
api_router.register_endpoint('slides', SlideViewSet)
api_router.register_endpoint('grades', GradeViewSet)
