from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import User
from .services import create_student, create_teacher, get_student, get_teacher, authenticate_user


class StudentCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {'name': 'John Doe',
                              'email': 'john@example.com', 'password': 'password'}

    def test_create_student(self):
        # Make the request
        url = reverse('create_student')
        response = self.client.post(
            url, data=self.valid_payload, format='json')

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'id': 1, **self.valid_payload})


class TeacherCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {'name': 'Jane Doe',
                              'email': 'jane@example.com', 'password': 'password'}

    def test_create_teacher(self):
        # Make the request
        url = reverse('create_teacher')
        response = self.client.post(
            url, data=self.valid_payload, format='json')

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'id': 1, **self.valid_payload})


class StudentDetailTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = User.objects.create(
            name='John Doe', email='john@example.com', password='password', role='student')

    def test_get_student(self):
        # Make the request
        url = reverse('student_detail', kwargs={'student_id': self.student.id})
        response = self.client.get(url)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
                         'id': self.student.id, 'name': 'John Doe', 'email': 'john@example.com'})

    def test_get_student_not_found(self):
        # Make the request with a non-existent student ID
        url = reverse('student_detail', kwargs={'student_id': 999})
        response = self.client.get(url)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TeacherDetailTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher = User.objects.create(
            name='Jane Doe', email='jane@example.com', password='password', role='teacher')

    def test_get_teacher(self):
        # Make the request
        url = reverse('teacher_detail', kwargs={'teacher_id': self.teacher.id})
        response = self.client.get(url)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
                         'id': self.teacher.id, 'name': 'Jane Doe', 'email': 'jane@example.com'})

    def test_get_teacher_not_found(self):
        # Make the request with a non-existent teacher ID
        url = reverse('teacher_detail', kwargs={'teacher_id': 999})
        response = self.client.get(url)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LoginViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='johndoe', email='john@example.com', password='password')

    def test_authenticate_user(self):
        # Make the request
        url = reverse('login')
        data = {'username': 'johndoe', 'password': 'password'}
        response = self.client.post(url, data=data)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.json())
        self.assertIn('access', response.json())

    def test_authenticate_user_invalid_credentials(self):
        # Make the request with invalid credentials
        url = reverse('login')
        data = {'username': 'johndoe', 'password': 'wrongpassword'}
        response = self.client.post(url, data=data)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.content.decode(), 'Invalid credentials')


class ServicesTests(TestCase):
    def test_create_student(self):
        # Call the service function
        student = create_student('John Doe', 'john@example.com', 'password')

        # Check the result
        self.assertEqual(student.name, 'John Doe')
        self.assertEqual(student.email, 'john@example.com')
        self.assertEqual(student.role, 'student')

    def test_create_teacher(self):
        # Call the service function
        teacher = create_teacher('Jane Doe', 'jane@example.com', 'password')

        # Check the result
        self.assertEqual(teacher.name, 'Jane Doe')
        self.assertEqual(teacher.email, 'jane@example.com')
        self.assertEqual(teacher.role, 'teacher')

    def test_get_student(self):
        # Create test data
        student = User.objects.create(
            name='John Doe', email='john@example.com', password='password', role='student')

        # Call the service function
        result = get_student(student.id)

        # Check the result
        self.assertEqual(result, student)

    def test_get_teacher(self):
        # Create test data
        teacher = User.objects.create(
            name='Jane Doe', email='jane@example.com', password='password', role='teacher')

        # Call the service function
        result = get_teacher(teacher.id)

        # Check the result
        self.assertEqual(result, teacher)

    def test_authenticate_user(self):
        # Create test data
        User.objects.create_user(
            username='johndoe', email='john@example.com', password='password')

        # Call the service function
        result = authenticate_user('johndoe', 'password')

        # Check the result
        self.assertIn('refresh', result)
        self.assertIn('access', result)

    def test_authenticate_user_invalid_credentials(self):
        # Call the service function with invalid credentials
        result = authenticate_user('johndoe', 'wrongpassword')

        # Check the result
        self.assertIsNone(result)
