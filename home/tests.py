from django.test import TestCase
from django.urls import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.db.models import signals
from .models import HomePage


class TestLoginRequiredDecorator(TestCase):
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
        page = HomePage.objects.first()

        response = page.serve(request)

        self.assertEqual(response.status_code, 200)
