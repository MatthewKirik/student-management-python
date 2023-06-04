from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import create_mark, update_mark, get_marks_by_course_and_date
from django.http import Http404
from StudentManagementAPI.permissions import IsTeacher
import json


class MarkUpdate(APIView):
    permission_classes = [IsTeacher]

    def post(self, request, mark_id, format=None):
        mark_value = request.data.get('mark_value')
        lesson_id = request.data.get('lesson_id')
        try:
            mark = update_mark(mark_id, mark_value, lesson_id)
            return Response(json.dumps(mark), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class MarksByCourseAndDate(APIView):
    permission_classes = [IsTeacher]

    def get(self, request, course_id, year, month, day, format=None):
        marks = get_marks_by_course_and_date(course_id, year, month, day)
        if marks:
            return Response(json.dumps(marks), status=status.HTTP_200_OK)
        else:
            return Response({"error": "Marks not found"}, status=status.HTTP_404_NOT_FOUND)


class MarkCreate(APIView):
    permission_classes = [IsTeacher]

    def post(self, request, format=None):
        course_id = request.data.get('course_id')
        student_id = request.data.get('student_id')
        date = request.data.get('date')  # 'YYYY-MM-DD'
        mark_value = request.data.get('mark_value')
        lesson_id = request.data.get('lesson_id')
        assessment_id = request.data.get('assessment_id')

        try:
            mark = create_mark(course_id, student_id, date,
                               mark_value, lesson_id, assessment_id)
            return Response(json.dumps(mark), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
