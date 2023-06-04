from datetime import date
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Mark
from .services import create_mark, update_mark, get_marks_by_course_and_date


class MarkUpdateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.mark = Mark.objects.create(mark_value=80, lesson_id=1)

    def test_update_mark(self):
        # Make the request
        url = reverse('update_mark', kwargs={'mark_id': self.mark.id})
        data = {'mark_value': 90, 'lesson_id': 2}
        response = self.client.post(url, data=data, format='json')

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
                         'id': self.mark.id, 'mark_value': 90, 'lesson_id': 2})

    def test_update_mark_not_found(self):
        # Make the request with a non-existent mark ID
        url = reverse('update_mark', kwargs={'mark_id': 999})
        data = {'mark_value': 90, 'lesson_id': 2}
        response = self.client.post(url, data=data, format='json')

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MarksByCourseAndDateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course_id = 1
        self.year = 2023
        self.month = 6
        self.day = 1

    def test_get_marks_by_course_and_date(self):
        # Create test data
        mark1 = Mark.objects.create(
            course_id=self.course_id, date=date(self.year, self.month, self.day))
        mark2 = Mark.objects.create(
            course_id=self.course_id, date=date(self.year, self.month, self.day))

        # Make the request
        url = reverse('get_marks_by_course_and_date', kwargs={'course_id': self.course_id,
                                                          'year': self.year,
                                                          'month': self.month,
                                                          'day': self.day})
        response = self.client.get(url)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{'id': mark1.id, 'course_id': self.course_id, 'date': f'{self.year}-{self.month:02d}-{self.day:02d}'},
                                           {'id': mark2.id, 'course_id': self.course_id, 'date': f'{self.year}-{self.month:02d}-{self.day:02d}'}])

    def test_get_marks_by_course_and_date_not_found(self):
        # Make the request for a non-existent course and date
        url = reverse('get_marks_by_course_and_date', kwargs={'course_id': self.course_id,
                                                          'year': 2022,
                                                          'month': 1,
                                                          'day': 1})
        response = self.client.get(url)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MarkCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
            'course_id': 1,
            'student_id': 1,
            'date': '2023-06-01',
            'mark_value': 80,
            'lesson_id': 1,
            'assessment_id': 1
        }

    def test_create_mark(self):
        # Make the request
        url = reverse('create_mark')
        response = self.client.post(
            url, data=self.valid_payload, format='json')

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'id': 1, **self.valid_payload})

    def test_create_mark_invalid_data(self):
        # Make the request with invalid data (missing required fields)
        url = reverse('create_mark')
        response = self.client.post(url, data={}, format='json')

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
