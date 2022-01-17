from django.db import models
from django.shortcuts import reverse, redirect
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel


class Announcement(models.Model):
    """
    A short message broadcast to students on the homepage.
    """

    date = models.DateField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        if len(self.text) > 28:
            return self.text[:25] + "..."
        return self.text


class HomePage(Page):
    """
    Landing page of the site.
    """

    max_count = 1

    def get_context(self, request):
        context: dict = super().get_context(request)
        course = request.user.enrollment.active_course
        context['course'] = course 
        context["announcement"] = Announcement.objects.latest("date")
        context["next_section"] = course.specific.next_section(request.user)
        return context

    def serve(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().serve(request, *args, **kwargs)
        return redirect(reverse('users:login'))


class NotEnrolled(Page):
    """
    Page redirected to when homepage is accessed, but student is not enrolled.
    """
    message = models.TextField()
    
    max_count = 1

    content_panels = Page.content_panels + [
        FieldPanel('message'),
    ]

