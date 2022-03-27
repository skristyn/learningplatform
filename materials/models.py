from typing import Callable, List, Optional
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework.serializers import Field
from wagtail.core.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.api import APIField
from wagtail.api.v2.utils import get_object_detail_url
from wagtail.core.query import PageQuerySet
from home.models import HomePage

"""
The first several block classes represent slide types.

These types should be developed with help from the fe folks to
best choose layout and design.
"""

class ResourceBlock(blocks.StructBlock):
    """
    For inserting a resource into the slides.
    """
    resource = ImageChooserBlock()


class HeadlineLeftImageBlock(blocks.StructBlock):
    """
    Headline across slide, image to the left, text to the right.
    """
    heading = blocks.CharBlock()
    image = ImageChooserBlock(required=True)
    body = blocks.RichTextBlock()

    class Meta:
        template = "materials/blocks/headline_left_image.html"


class ImageTopBlock(blocks.StructBlock):
    """
    Image across the top, text across the bottom.        
    """
    image = ImageChooserBlock(required=True)
    body = blocks.RichTextBlock()

    class Meta:
        template = "materials/blocks/image_top.html"


class ImageRightBlock(blocks.StructBlock):
    """
    Image on the right, text on the left.
    """
    image = ImageChooserBlock(required=True)
    body = blocks.RichTextBlock()

    class Meta:
        template = "materials/blocks/image_right.html"


class UrlSerializer(Field):
    def to_representation(self, parent: Page) -> List[dict]:
        request = self.context["request"]

        return get_object_detail_url(
                    self.context["router"], request, Lesson, parent.pk
                )


class Resource(Page):
    """
    A resource is a special slide that can be linked to from the
    resource kit.
    """
    
    description = models.TextField(blank=True, null=True)
    topic = models.TextField(blank=True, null=True)
    parent_page_types = ["materials.Section"]
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("description"),
    ]


class CompletedSerializer(Field):
    """
    Originally written to suply the request's user object to the completed method from
    both the lesson and section classes. Should rename because it can be used to supply
    the user to any model method.
    """

    def to_representation(self, func: Callable[[User], bool]) -> bool:
        student = self.context["request"].user
        return func(student)


class Section(RoutablePageMixin, Page):
    """
    The section is the core informational unit of the platform. Once a student
    begins a section they are brought into the learning Vue application.
    """

    description = models.TextField(null=True, blank=True)
    time_to_complete = models.IntegerField(blank=True, null=True)
    parent_page_types = ["materials.Lesson"]

    slides = StreamField([
        ('resource', ResourceBlock()),
        ('headlineleftimage', HeadlineLeftImageBlock()),
        ('imagetopblock', ImageTopBlock()),
        ('imagerightblock', ImageRightBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("time_to_complete"),
        StreamFieldPanel("slides"),
    ]

    api_fields = [
        APIField("title"),
        APIField("description"),
        APIField("lesson_id"),
        APIField("lesson_url", serializer=UrlSerializer()),
        APIField("number"),
        APIField("time_to_complete"),
        APIField("completed", serializer=CompletedSerializer()),
        APIField("slides"),
    ]

    @property
    def number(self) -> int:
        """
        This computes the lesson number based on position in the tree vs hard code.
        Requiring a db look up on a property is gauche though maybe...
        """
        return len(self.get_prev_siblings()) + 1

    @property
    def lesson_url(self) -> int:
        return self.get_parent()

    @property
    def lesson_id(self) -> int:
        return self.get_parent().id
    
    def get_context(self, request) -> dict:
        """
        Append the slide pages to the context provided to the template.
        """
        context: dict = super().get_context(request)
        context["slides"] = self.slides
        context["home_page"] = HomePage.objects.first()
        context["textbook"] = self.course
        return context

    def serve(self, request, *args, **kwargs):
        """
        Overwriting the serve method to allow for a post request marking the
        section as complete for the user.
        """
        if request.method == "POST":
            self._mark_complete(request.user)
            return redirect(self.url + "congratulations")
        return super().serve(request, *args, **kwargs)

    @route(r"^congratulations")
    def serve_congratulations(self, request):
        """
        This serves the same model, but to a different template to congratulate
        the user on completing the lesson.
        """
        return self.render(request, template="materials/congratulations.html")

    def completed(self, student: User) -> bool:
        """
        Checks if a grade exists for the student--because we're doing simple
        'mark completed' grading that's all we need to do
        """
        return self.grade_set.filter(student=student).exists()  # type: ignore

    @property
    def course(self) -> Page:
        return self.get_parent().get_parent()

    def _mark_complete(self, student: User) -> None:
        Grade.objects.get_or_create(section=self, student=student)


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
                "description": section.specific.description,
                "completed": section.specific.completed(request.user),
                "section_num": section.specific.number,
                "time_to_complete": section.specific.time_to_complete,
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
        APIField("description"),
        APIField("number"),
        APIField("completed", serializer=CompletedSerializer()),
        APIField("sections", serializer=SectionsSerializer()),
        APIField("time_remaining", serializer=CompletedSerializer()),
    ]

    @property
    def sections(self) -> PageQuerySet:
        return self.get_children().public().live()

    @property
    def number(self) -> int:
        """
        This computes the lesson number based on position in the tree vs hard code.
        Requiring a db look up on a property is gauche though maybe...
        """
        return len(self.get_prev_siblings()) + 1

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

    def next_section(self, student: User) -> Optional[Section]:
        """
        Returns the next section that is not complete, and if the whole lesson has
        been finished it returns None.
        """
        if self.completed(student):
            return None
        return next(
            filter(
                lambda section: not section.specific.completed(student),
                self.get_children(),
            )
        )

    def time_remaining(self, student: User) -> int:
        return sum(
            section.specific.time_to_complete
            for section in self.get_children()
            if not section.specific.completed(student)
        )

    def _mark_complete(self, student: User) -> None:
        """
        Mark all sections complete for the lesson. For testing.
        """

        for section in self.sections:
            section.specific._mark_complete(student)


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
                "lesson_num": lesson.specific.number,
                "title": lesson.title,
                "completed": lesson.specific.completed(request.user),
                "time_remaining": lesson.specific.time_remaining(request.user),
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

    description = models.TextField(null=True, blank=True)
    subpage_types = ["materials.Lesson"]
    max_count = 1

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]

    api_fields = [
        APIField("title"),
        APIField("description"),
        APIField("lessons", serializer=LessonsSerializer()),
        APIField("completed", serializer=CompletedSerializer()),
    ]

    @property
    def lessons(self):
        """
        All publsihed lessons for the textbook.
        """
        return self.get_children().public().live()

    @property
    def first_section(self):
        """
        Return the first section of the course.
        """
        first_lesson: Lesson = self.get_children().first()
        return first_lesson.get_children().first()

    def get_context(self, request) -> dict:
        """
        Append the lesson pages to the context provided to the template.
        """

        context = super().get_context(request)
        context["lessons"] = self.lessons
        context["home_page"] = HomePage.objects.first()
        context["next_section"] = self.next_section(request.user)
        context["time_remaining"] = self.time_remaining(request.user)
        return context

    def completed(self, student: User) -> bool:
        """
        For now we have to 1+n it, because going to deep in the treebeard hierarchy with
        prefetch_related is confusing.
        """

        return all(lesson.specific.completed(student) for lesson in self.get_children())

    def time_remaining(self, student: User) -> int:
        """
        Return the time remaining for the entire course. This needs to be rewritten to have
        a more effecient query.
        """
        return sum(
            lesson.specific.time_remaining(student) for lesson in self.get_children()
        )

    def next_section(self, student: User) -> Optional[Section]:
        """
        Returns the next incomplete section for the user, unless course is compelte, then None.
        """
        lesson = next(
            filter(
                lambda lesson: lesson.specific.next_section(student) is not None,
                self.get_children(),
            ),
            None,
        )
        if lesson is None:
            return self.first_section
        return lesson.specific.next_section(student)


