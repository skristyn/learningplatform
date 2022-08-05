import json
from django.test import TestCase
from django.urls import reverse
from django.test.client import RequestFactory
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser, User
from django.db.models import signals
from .models import HomePage, Announcement
from users.models import Enrollment
from materials.models import Textbook
from materials.tests import build_lesson


class TestAPIToken(TestCase):
    def setUp(self):
        lesson = build_lesson()
        user = User.objects.create(
                username="easy",
        )
        user.set_password("easy")
        user.save()
    
    def test_token_available(self):
        self.assertTrue(Token.objects.all())
    
    def test_success(self):
        response = self.client.get("/api/v1")

    def test_get_token(self):
        response = self.client.post(
            "/api/v1/token-auth",
            data={"username": "easy", "password": "easy"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)["token"],
            Token.objects.first().key,
        )

    def test_use_token(self):
        token_response = self.client.post(
            "/api/v1/token-auth",
            data={"username": "easy", "password": "easy"},
        )

        token = json.loads(token_response.content)["token"]
        response = self.client.get(
            "/api/v1/lessons/",
            {"Authorization": f"Token {token}"},
        )
        
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)

        print(content)

        self.assertEqual(content["items"][0]["type"], "materials.Lesson")



