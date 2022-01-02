import logging
import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import signals
from rest_framework.test import APITestCase
from .models import Section, Grade, Lesson, Textbook


logging.basicConfig(filename="testing.log", filemode="w", level=logging.DEBUG)


def build_lesson(title="Lesson One", parent=None):
    if not parent:
        lesson: Lesson = Lesson.add_root(title=title)
    else:
        lesson = Lesson(title=title)
        parent.add_child(instance=lesson)
    section_one: Section = Section(title=f"{lesson.title}-Section one")
    section_two: Section = Section(title=f"{lesson.title}-Section two")
    lesson.add_child(instance=section_one)
    lesson.add_child(instance=section_two)

    return lesson


def build_student():
    return User.objects.create(username="harvey", password="badpass")


class TestGrade(TestCase):
    def setUp(self):
        signals.post_save.disconnect(sender=User, dispatch_uid="irrelevant")

    def test_create_grade(self):
        section: Section = Section.add_root(title="First title")
        student: User = User.objects.create(username="harvey")

        Grade.objects.create(student=student, section=section)

        self.assertTrue(section.grade_set.all())

    def test_check_section_completion(self):
        section: Section = Section.add_root(title="First title")
        student: User = User.objects.create(username="harvey")
        Grade.objects.create(student=student, section=section)

        result = section.completed(student)

        self.assertTrue(result)

    def test_check_section_completion_false(self):
        section: Section = Section.objects.create(
            title="First title", path="1010", depth=2
        )
        student: User = User.objects.create(username="harvey")

        result = section.completed(student)

        self.assertFalse(result)

    def test_check_lesson_completion(self):
        lesson = build_lesson()
        student = build_student()

        lesson._mark_complete(student)

        result = lesson.completed(student)

        self.assertTrue(result)

    def test_check_lesson_completetion_false(self):
        lesson = build_lesson()
        student = build_student()

        result = lesson.completed(student)

        self.assertFalse(result)

    def test_check_lesson_completion_partial(self):
        lesson = build_lesson()
        student = build_student()
        Grade.objects.create(
            student=student, section=lesson.get_children().specific().first()
        )

        result = lesson.completed(student)

        self.assertFalse(result)

    def test_course_complete(self):
        course = Textbook.add_root(title="test textbook")
        lesson = build_lesson(parent=course)
        lesson_two = build_lesson(title="second", parent=course)
        student = build_student()

        lesson._mark_complete(student)
        lesson_two._mark_complete(student)

        result = course.completed(student)

        self.assertTrue(result)

    def test_course_complete_false(self):
        course = Textbook.add_root(title="test textbook")
        lesson = build_lesson(parent=course)
        lesson_two = build_lesson(title="second", parent=course)
        student = build_student()
        lesson._mark_complete(student)

        result = course.completed(student)

        self.assertFalse(result)


class TestAPI(APITestCase):
    logger = logging.getLogger("tests.api")

    def setUp(self):
        signals.post_save.disconnect(sender=User, dispatch_uid="irrelevant")

    def test_lesson_endpoint_is_not_empty(self):
        lesson = build_lesson()
        student = build_student()
        response = self.client.get("/api/v1/lessons/")
        content = json.loads(response.content)
        self.assertEqual(lesson.id, content["items"][0]["id"])

    def test_section_endpoint_is_not_empty(self):
        lesson = build_lesson()
        student = build_student()
        response = self.client.get("/api/v1/sections/")
        content = json.loads(response.content)

        # This is fragile, change it.
        self.assertEqual(
            lesson.get_children().specific().first().id, content["items"][0]["id"]
        )

    def test_lesson_sections(self):
        pass

    def test_lesson_detail_endpoint(self):
        pass

    def test_section_detail_endpoint(self):
        pass

    def test_section_completed(self):
        lesson = build_lesson()
        student = build_student()
        section = lesson.get_children().specific().first()
        Grade.objects.create(student=student, section=section)
        self.client.force_login(user=student)

        response = self.client.get(f"/api/v1/sections/{section.id}/")

        content = json.loads(response.content)
        self.logger.info(content)

        self.assertTrue(content["completed"])

    def test_section_not_completed(self):
        lesson = build_lesson()
        student = build_student()
        section = lesson.get_children().specific().first()
        self.client.force_login(user=student)

        response = self.client.get(f"/api/v1/sections/{section.id}/")

        content = json.loads(response.content)
        self.assertFalse(content["completed"])

    def test_lesson_completed(self):
        lesson = build_lesson()
        student = build_student()
        for section in lesson.get_children().specific():
            Grade.objects.create(student=student, section=section)
        self.client.force_login(user=student)

        response = self.client.get(f"/api/v1/lessons/{lesson.id}/")

        content = json.loads(response.content)
        self.logger.info(content)

        self.assertTrue(content["completed"])

    def test_lesson_not_completed(self):
        lesson = build_lesson()
        student = build_student()
        self.client.force_login(user=student)

        response = self.client.get(f"/api/v1/lessons/{lesson.id}/")

        content = json.loads(response.content)
        self.logger.info(content)

        self.assertFalse(content["completed"])

    def test_lesson_partial_completed(self):
        lesson = build_lesson()
        student = build_student()
        section = lesson.get_children().specific().first()
        Grade.objects.create(student=student, section=section)
        self.client.force_login(user=student)

        response = self.client.get(f"/api/v1/lessons/{lesson.id}/")

        content = json.loads(response.content)
        self.logger.info(content)

        self.assertFalse(content["completed"])

    def test_grade_post(self):
        section = Section.add_root(title="Section one")
        student = User.objects.create(username="harvey")
        self.client.force_login(user=student)

        response = self.client.post(
            "/api/v1/grades/", {"section": section.id, "student": student.id}
        )

        self.assertTrue(Grade.objects.filter(section=section, student=student))
