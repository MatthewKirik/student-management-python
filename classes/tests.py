from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Class
from .services import create_class, assign_students_to_class, get_teacher_course_classes, get_class


class ClassCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {'name': 'New Class'}

    def test_create_class(self):
        # Make the request
        url = reverse('create_class')
        response = self.client.post(
            url, data=self.valid_payload, format='json')

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'id': 1, 'name': 'New Class'})


class StudentsToClassAssignmentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.class_ = Class.objects.create(name='Class 1')
        self.student_ids = [1, 2]

    def test_assign_students_to_class(self):
        # Make the request
        url = reverse('assign_students_to_class',
                      kwargs={'class_id': self.class_.id})
        data = {'student_ids': self.student_ids}
        response = self.client.post(url, data=data, format='json')

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
                         'id': self.class_.id, 'name': 'Class 1', 'students': []})

    def test_assign_students_to_class_invalid_class(self):
        # Make the request with a non-existent class ID
        url = reverse('assign_students_to_class', kwargs={'class_id': 999})
        data = {'student_ids': self.student_ids}
        response = self.client.post(url, data=data, format='json')

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TeacherCourseClassesListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher_id = 1
        self.course_id = 1

    def test_get_teacher_course_classes(self):
        # Create test data
        class1 = Class.objects.create(name='Class 1')
        class2 = Class.objects.create(name='Class 2')

        # Make the request
        url = reverse('class_detail',
                      kwargs={'teacher_id': self.teacher_id, 'course_id': self.course_id})
        response = self.client.get(url)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{'id': class1.id, 'name': 'Class 1'}, {
                         'id': class2.id, 'name': 'Class 2'}])


class ClassDetailTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.class_ = Class.objects.create(name='Class 1')

    def test_get_class(self):
        # Make the request
        url = reverse('class-detail', kwargs={'class_id': self.class_.id})
        response = self.client.get(url)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
                         'id': self.class_.id, 'name': 'Class 1', 'students': []})

    def test_get_class_not_found(self):
        # Make the request with a non-existent class ID
        url = reverse('class-detail', kwargs={'class_id': 999})
        response = self.client.get(url)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ServicesTests(TestCase):
    def test_create_class(self):
        # Call the service function
        class_ = create_class('New Class')

        # Check the result
        self.assertEqual(class_.name, 'New Class')

    def test_assign_students_to_class(self):
        # Create test data
        class_ = Class.objects.create(name='Class 1')
        student_ids = [1, 2]

        # Call the service function
        result = assign_students_to_class(class_.id, student_ids)

        # Check the result
        self.assertEqual(result, class_)
        self.assertEqual(list(class_.students.all()), [])

    def test_get_teacher_course_classes(self):
        # Create test data
        teacher_id = 1
        course_id = 1
        class1 = Class.objects.create(name='Class 1')
        class1.courses.add(course_id)
        class2 = Class.objects.create(name='Class 2')
        class2.courses.add(course_id)

        # Call the service function
        classes = get_teacher_course_classes(teacher_id, course_id)

        # Check the result
        self.assertEqual(list(classes), [class1, class2])

    def test_get_class(self):
        # Create test data
        class_ = Class.objects.create(name='Class 1')

        # Call the service function
        result = get_class(class_.id)

        # Check the result
        self.assertEqual(result, class_)
