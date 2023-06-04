from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Course
from classes.models import Class
from .services import get_teacher_courses, create_course, assign_class_to_course, get_course


class TeacherCoursesListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher_id = 1

    def test_get_teacher_courses(self):
        # Create test data
        course1 = Course.objects.create(
            name="Course 1", teacher_id=self.teacher_id)
        course2 = Course.objects.create(
            name="Course 2", teacher_id=self.teacher_id)

        # Make the request
        url = reverse('teacher-courses',
                      kwargs={'teacher_id': self.teacher_id})
        response = self.client.get(url)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{'id': course1.id, 'name': 'Course 1'}, {
                         'id': course2.id, 'name': 'Course 2'}])


class CourseCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
            'name': 'New Course',
            'description': 'Course Description',
            'teacher_id': 1
        }

    def test_create_course(self):
        # Make the request
        url = reverse('create_course')
        response = self.client.post(
            url, data=self.valid_payload, format='json')

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
                         'id': 1, 'name': 'New Course', 'description': 'Course Description', 'teacher_id': 1})


class ClassToCourseAssignmentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(name="Course 1", teacher_id=1)
        self.class_id = 1

    def test_assign_class_to_course(self):
        # Make the request
        url = reverse('assign_class_to_course',
                      kwargs={'course_id': self.course.id, 'class_id': self.class_id})
        response = self.client.post(url)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
                         'id': self.course.id, 'name': 'Course 1', 'classes': [self.class_id]})


class CourseDetailTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(name="Course 1", teacher_id=1)

    def test_get_course(self):
        # Make the request
        url = reverse('course-detail', kwargs={'course_id': self.course.id})
        response = self.client.get(url)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
                         'id': self.course.id, 'name': 'Course 1'})


class ServicesTests(TestCase):
    def test_get_teacher_courses(self):
        # Create test data
        teacher_id = 1
        course1 = Course.objects.create(name="Course 1", teacher_id=teacher_id)
        course2 = Course.objects.create(name="Course 2", teacher_id=teacher_id)

        # Call the service function
        courses = get_teacher_courses(teacher_id)

        # Check the result
        self.assertEqual(list(courses), [course1, course2])

    def test_create_course(self):
        # Call the service function
        course = create_course('New Course', 'Course Description', teacher=1)

        # Check the result
        self.assertEqual(course.name, 'New Course')
        self.assertEqual(course.description, 'Course Description')
        self.assertEqual(course.teacher, 1)

    def test_assign_class_to_course(self):
        # Create test data
        course = Course.objects.create(name="Course 1", teacher_id=1)
        class_ = Class.objects.create(name="Class 1")

        # Call the service function
        result = assign_class_to_course(course.id, class_.id)

        # Check the result
        self.assertEqual(result, course)
        self.assertEqual(list(course.classes.all()), [class_])

    def test_get_course(self):
        # Create test data
        course = Course.objects.create(name="Course 1", teacher_id=1)

        # Call the service function
        result = get_course(course.id)

        # Check the result
        self.assertEqual(result, course)
