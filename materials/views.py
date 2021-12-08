from django.shortcuts import render
from wagtail.api.v2.views import BaseAPIViewSet
from .models import Lesson, Section


class LessonViewSet(BaseAPIViewSet):
    model = Lesson


class SectionViewSet(BaseAPIViewSet):
    model = Section
