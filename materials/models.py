from django.db import models
from django.contrib.auth.models import User
from wagtail.core.models import Page


class Textbook(Page):
    """The textbook class is the main container for the entire course
       it holds only the key data."""

    subpage_types = ['materials.Lesson']


class Lesson(Page):
    """The lesson groups several sections for organization and reporting student 
       progress through the material."""

    parent_page_types = ['materials.Textbook']
    subpage_types =['materials.Section']

    def check_work_of(self, student: User):
        return not (self.get_children()
                        .prefetch_related('grade_set')
                        .exclude(section__grade__student=student)
                        .exists())


class Section(Page):
    """The section is the core informational unit of the platform. Once a student
       begins a section they are brought into the learning Vue application."""

    parent_page_types = ['materials.Lesson']
    subpage_types = ['materials.Slide', 'materials.Resource']

    def check_work_of(self, student: User):
        return self.grade_set.filter(student=student).exists()


class Slide(Page):
    """A section comprises several slides. They're where the information is
       added and displayed."""

    parent_page_types = ['materials.Section']


class Resource(Page):
    """A resource is a special slide that can be linked back to from the
       resource kit."""


class Grade(models.Model):
    """The grade is a simple entry that shows a User has marked a Section 
       complete."""
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['student', 'section']