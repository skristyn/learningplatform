from django.test import TestCase
from rest_framework.authtoken.models import Token
from .models import User, Profile


class TestToken(TestCase):
    def setUp(self):
        User.objects.create(username="harvey", password="canned_gold")

    def test_user_created(self):
        self.assertTrue(User.objects.all())

    def test_profile_exists(self):
        self.assertTrue(Profile.objects.all())

    def test_token_exists(self):
        self.assertTrue(Token.objects.all())


class TestUser(TestCase):
    pass


class TestProfile(TestCase):
    pass


class TestTeam(TestCase):
    pass
