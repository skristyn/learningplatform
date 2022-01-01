from typing import Callable, List
from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from rest_framework.serializers import Field
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.api import APIField
from wagtail.api.v2.utils import get_object_detail_url
from wagtail.core.query import PageQuerySet
from home.models import wagtail_require_login


"""
NOTE: The overwriting of the serve function with the wagtail_require_login decorator wont
be necessary once the course front end has moved to Vue. This is just to serve the template
pages in the meantime.
"""


class Slide(Page):
    """
    A section comprises several slides. They're where the information is
    added and displayed.
    """

    parent_page_types = ["materials.Section"]
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    api_fields = [
        APIField("title"),
        APIField("body"),
    ]


class SlideSerializer(Field):
    """
    Packages the slide data, most importantly the detail_url, to be displayed
    on the section views.
    """

    def to_representation(self, slides: List[Slide]) -> List[dict]:
        request = self.context["request"]

        return [
            {
                "id": slide.id,
                "title": slide.title,
                "detail_url": get_object_detail_url(
                    self.context["router"], request, Slide, slide.pk
                ),
            }
            for slide in slides
        ]


class Resource(Page):
    """
    A resource is a special slide that can be linked to from the
    resource kit.
    """

    parent_page_types = ["materials.Section"]
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class CompletedSerializer(Field):
    """
    Supplies the user object to the completed method from both the
    lesson and section classes.
    """

    def to_representation(self, func: Callable[[User], bool]) -> bool:
        student = self.context["request"].user
        return func(student)


class Section(Page):
    """
    The section is the core informational unit of the platform. Once a student
    begins a section they are brought into the learning Vue application.
    """

    parent_page_types = ["materials.Lesson"]
    subpage_types = ["materials.Slide", "materials.Resource"]

    api_fields = [
        APIField("title"),
        APIField("completed", serializer=CompletedSerializer()),
        APIField("slides", serializer=SlideSerializer()),
    ]

    @property
    def slides(self):
        return self.get_children().public().live()

    def completed(self, student: User) -> bool:
        """
        Checks if a grade exists for the student--because we're doing simple
        'mark completed' grading that's all we need to do
        """
        return self.grade_set.filter(student=student).exists()  # type: ignore

    def get_context(self, request) -> dict:
        """
        Append the slide pages to the context provided to the template.
        """
        context: dict = super().get_context(request)
        context["slides"] = self.slides
        return context

    def _mark_complete(self, student: User) -> None:
        Grade.objects.create(section=self, student=student)
    
    @wagtail_require_login
    def serve(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        response: HttpResponse = super().serve(request, *args, **kwargs)
        return response


class SectionsSerializer(Field):
    """
    Serializes the section page model for display on the lesson view, pulls
    the request context to feed the logged-in user to the completed method.
    """

    def to_representation(self, sections: List[Section]) -> List[dict]:
        request = self.context["request"]

        return [
            {
                "id": section.id,
                "title": section.title,
                "completed": section.specific.completed(request.user),
                "detail_url": get_object_detail_url(
                    self.context["router"], request, Section, section.pk
                ),
            }
            for section in sections
        ]


class Lesson(Page):
    """
    The lesson groups several sections for organization and reporting student
    progress through the material. You could think of it as a chapter in a text
    book or a unit in a school course.
    """

    description = models.TextField(blank=True, null=True)  # type: ignore
    parent_page_types = ["materials.Textbook"]
    subpage_types = ["materials.Section"]

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]

    api_fields = [
        APIField("title"),
        APIField("completed", serializer=CompletedSerializer()),
        APIField("sections", serializer=SectionsSerializer()),
    ]

    @property
    def sections(self) -> PageQuerySet:
        return self.get_children().public().live()

    def completed(self, student: User) -> bool:
        """
        Look for a section that isn't connected to the student thdrough
        a grade.
        """
        return not (
            self.get_children()
            .prefetch_related("grade_set")
            .exclude(section__grade__student=student)
            .exists()
        )

    def get_context(self, request) -> dict:
        """
        Append the section pages to the context provided to the template.
        """
        context: dict = super().get_context(request)
        context["sections"] = self.sections
        return context

    def _mark_complete(self, student: User) -> None:
        """
        Mark all sections complete for the lesson. For testing.
        """

        for section in self.sections:
            section.specific._mark_complete(student)
    
    @wagtail_require_login
    def serve(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        response: HttpResponse = super().serve(request, *args, **kwargs)
        return response


class LessonsSerializer(Field):
    """
    Serializes the lesson page model like the SectionsSerializer.
    """

    def to_representation(self, lessons: List[Lesson]) -> List[dict]:
        """
        The current context must be added to the sections serializer instance context.
        There is probably a better way to do this, but for now this will suffice.
        """
        request = self.context["request"]

        # !
        sections_serializer = SectionsSerializer()
        sections_serializer._context = self.context

        return [
            {
                "id": lesson.id,
                "title": lesson.title,
                "completed": lesson.specific.completed(request.user),
                "detail_url": get_object_detail_url(
                    self.context["router"], request, Lesson, lesson.pk
                ),
                "sections": sections_serializer.to_representation(
                    lesson.specific.sections
                ),
            }
            for lesson in lessons
        ]


class Grade(models.Model):
    """
    The grade is a simple entry that shows a User has marked a Section
    complete.
    """

    student: User = models.ForeignKey(User, on_delete=models.CASCADE)
    section: Section = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["student", "section"]

    def __str__(self) -> str:
        return f"{self.section.title} marked complete for {self.student.username}"


class Textbook(Page):
    """
    The container for the all course materials.
    """

    subpage_types = ["materials.Lesson"]
    max_count = 1

    api_fields = [
        APIField("title"),
        APIField("lessons", serializer=LessonsSerializer()),
    ]

    @property
    def lessons(self):
        return self.get_children().public().live()

    def get_context(self, request):
        """
        Append the lesson pages to the context provided to the template.
        """
        
        context = super().get_context(request)
        context["lessons"] = self.lessons
        return context

    def completed(self, student: User) -> bool:
        """
        For now we have to 1+n it, because going to deep in the treebeard hierarchy with
        prefetch_related is confusing.
        """

        return all(lesson.specific.completed(student) for lesson in self.get_children())
    
    @wagtail_require_login
    def serve(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        response: HttpResponse = super().serve(request, *args, **kwargs)
        return response

