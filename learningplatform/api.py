from wagtail.api.v2.router import WagtailAPIRouter
from materials.views import LessonViewSet, SectionViewSet, GradeViewSet

api_router = WagtailAPIRouter('learningplatformapi')

api_router.register_endpoint('lessons', LessonViewSet)
api_router.register_endpoint('sections', SectionViewSet)
api_router.register_endpoint('grades', GradeViewSet)