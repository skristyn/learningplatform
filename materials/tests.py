from django.test import TestCase
from django.contrib.auth.models import User
from .models import Section, Grade, Lesson


def build_lesson():
    lesson: Lesson = Lesson.add_root(title='Lesson One')
    section_one: Section = Section(title='Section one')
    section_two: Section = Section(title='Section two')
    lesson.add_child(instance=section_one)
    lesson.add_child(instance=section_two)
    student = User.objects.create(username='harvey')

    return lesson, student


class TestGrade(TestCase):
    def test_create_grade(self):
        section: Section = Section.add_root(title='First title')
        student: User = User.objects.create(username='harvey')

        Grade.objects.create(student=student, section=section)

        self.assertTrue(section.grade_set.all())

    def test_check_section_completion(self):
        section: Section = Section.add_root(title='First title')
        student: User = User.objects.create(username='harvey')
        Grade.objects.create(student=student, section=section)

        result = section.check_work_of(student)

        self.assertTrue(result)

    def test_check_section_completion_false(self):
        section: Section = Section.objects.create(title='First title', path='1010', depth=2)
        student: User = User.objects.create(username='harvey')

        result = section.check_work_of(student)

        self.assertFalse(result)

    def test_check_lesson_completion(self):
        lesson, student = build_lesson()
        for section in lesson.get_children().specific():
            Grade.objects.create(student=student, section=section)
        
        result = lesson.check_work_of(student)

        self.assertTrue(result)

    def test_check_lesson_completetion_false(self):
        lesson, student = build_lesson()

        result = lesson.check_work_of(student)

        self.assertFalse(result)

    def test_check_lesson_completion_partial(self):
        lesson, student = build_lesson()
        Grade.objects.create(student=student, section=lesson.get_children().specific().first())

        result = lesson.check_work_of(student)

        self.assertFalse(result)


class TestAPI(TestCase):
    pass