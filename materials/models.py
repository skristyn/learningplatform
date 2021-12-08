from typing import Callable, List
from django.db import models
from django.contrib.auth.models import User
from rest_framework.serializers import Field
from wagtail.core.models import Page
from wagtail.api import APIField
from wagtail.core.query import PageQuerySet


class Textbook(Page):
    """The textbook class is the main container for the entire course
       it holds only the key data."""

    subpage_types = ['materials.Lesson']
    max_count = 1


class CompletedSerializer(Field):
    """Supplies the user object to the completed method from both the 
       lesson and section classes. Feels like an antipattern, but it
       does the trick."""
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
        APIField('completed', serializer=CompletedSerializer())
    ]

    def completed(self, student: User):
        return self.grade_set.filter(student=student).exists()


class SectionSerializer(Field):
    def to_representation(self, sections: List[Section]) -> List[dict]:
        student = self.context['request'].user
        return [
            {
                'id': section.id,
                'title': section.title,
                'url': section.url,
                'completed': section.specific.completed(student),
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
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['student', 'section']
