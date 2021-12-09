from typing import Callable, List
from django.db import models
from django.contrib.auth.models import User
from rest_framework.serializers import Field
from wagtail.core.models import Page
from wagtail.api import APIField
from wagtail.api.v2.utils import get_object_detail_url
from wagtail.core.query import PageQuerySet


class Textbook(Page):
    """The textbook class is the main container for the entire course
       it holds only the key data."""

    subpage_types = ['materials.Lesson']
    max_count = 1


class CompletedSerializer(Field):
    """Supplies the user object to the completed method from both the 
       lesson and section classes."""
    def to_representation(self, func: Callable):
        student = self.context['request'].user
        return func(student)


class Section(Page):
    """The section is the core informational unit of the platform. Once a student
       begins a section they are brought into the learning Vue application."""

    parent_page_types = ['materials.Lesson']
    subpage_types = ['materials.Slide', 'materials.Resource']

    api_fields = [
        APIField('title'),
        APIField('completed', serializer=CompletedSerializer()),
    ]

    def completed(self, student: User):
        return self.grade_set.filter(student=student).exists()


class SectionSerializer(Field):
    def to_representation(self, sections: List[Section]) -> List[dict]:
        request = self.context['request']
        
        return [
            {
                'id': section.id,
                'title': section.title,
                'detail_url': get_object_detail_url(
                    self.context['router'], request, Section, section.pk
                    ),
                'completed': section.specific.completed(request.user),
            } for section in sections
        ]


class Lesson(Page):
    """The lesson groups several sections for organization and reporting student 
       progress through the material."""

    parent_page_types = ['materials.Textbook']
    subpage_types = ['materials.Section']

    api_fields = [
        APIField('title'),
        APIField('completed', serializer=CompletedSerializer()),
        APIField('sections', serializer=SectionSerializer()),
    ]

    @property
    def sections(self) -> PageQuerySet:
        return self.get_children().public().live()

    def completed(self, student: User) -> bool:
        """Look for a section that isn't connected to the student 
           through a grade."""
        return not (self.get_children()
                        .prefetch_related('grade_set')
                        .exclude(section__grade__student=student)
                        .exists())


class Slide(Page):
    """A section comprises several slides. They're where the information is
       added and displayed."""

    parent_page_types = ['materials.Section']


class Resource(Page):
    """A resource is a special slide that can be linked back to from the
       resource kit."""
    
    parent_page_types = ['materials.Section']


class Grade(models.Model):
    """The grade is a simple entry that shows a User has marked a Section 
       complete."""
    student: User = models.ForeignKey(User, on_delete=models.CASCADE)
    section: Section = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['student', 'section']

    def __str__(self):
        return f'{self.section.title} marked complete for {self.student.username}'
