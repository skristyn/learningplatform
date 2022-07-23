from django.test import TestCase
from django.urls import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.db.models import signals
from .models import HomePage, Announcement
from users.models import Enrollment
from materials.models import Textbook
from materials.tests import build_lesson


class TestLoginRequired(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_redirect(self):
        """
        Does an unauthenticated user get redirected?

        The 'user' attribute on the request class is set by middleware,
        so you have to set it yourself.
        """
        request = self.factory.get("/")
        request.user = AnonymousUser()
        page = HomePage.objects.first()

        response = page.serve(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login"))

    def test_success(self):
        """
        Does an unauthenticated user get redirected?

        The 'user' attribute on the request class is set by middleware,
        so you have to set it yourself.
        """
        signals.post_save.disconnect(sender=User, dispatch_uid="irrelevant")
        request = self.factory.get("/")
        request.user = User.objects.create(username="Harvey")
        announcement = Announcement.objects.create(text="Test announcement")
        page = HomePage.objects.first()
        textbook = Textbook.add_root(title="Big book")
        build_lesson(parent=textbook)

        enrollment = Enrollment.objects.create(
            user=request.user, active_course=textbook
        )
        response = page.serve(request)

        self.assertEqual(response.status_code, 200)
