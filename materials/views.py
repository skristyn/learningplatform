from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import path
from django.contrib.auth.models import User
from wagtail.api.v2.views import BaseAPIViewSet
from .models import Lesson, Section, Grade


class LessonViewSet(BaseAPIViewSet):
    model = Lesson


class SectionViewSet(BaseAPIViewSet):
    model = Section


class GradeViewSet(BaseAPIViewSet):
    model = Grade

    @classmethod
    def get_urlpatterns(cls):
        """
        This returns a list of URL patterns for the endpoint
        """
        return [
            path('', cls.as_view({'get': 'listing_view', 'post': 'create_grade'}), name='listing'),
            path('<int:pk>/', cls.as_view({'get': 'detail_view'}), name='detail'),
            path('find/', cls.as_view({'get': 'find_view'}), name='find'),
        ]
    
    def create_grade(self, request):
        student = get_object_or_404(User, pk=request.POST['student'])
        section = get_object_or_404(Section, pk=request.POST['section'])
        Grade.objects.create(student=student, section=section)

        return JsonResponse(
            {'message': f'{section.title} was marked completed for {student.username}'}
            )