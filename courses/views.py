import json
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from StudentManagementAPI.permissions import IsHead, IsTeacher
from .services import get_teacher_courses, create_course, assign_class_to_course, get_course
from .models import Course
from .serializers import CourseSerializer


class TeacherCoursesList(APIView):
    permission_classes = [IsTeacher]

    def get(self, request, teacher_id, format=None):
        courses = get_teacher_courses(teacher_id)
        return Response(CourseSerializer(courses, many=True).data, status=status.HTTP_200_OK)


class CourseCreate(APIView):
    permission_classes = [IsHead]

    def post(self, request, format=None):
        name = request.data.get('name')
        description = request.data.get('description')
        teacher_id = request.data.get('teacher_id')
        try:
            course = create_course(name, description, teacher_id)
            return Response(json.dumps(course), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ClassToCourseAssignment(APIView):
    permission_classes = [IsHead]

    def post(self, request, course_id, class_id, format=None):
        try:
            course = assign_class_to_course(course_id, class_id)
            return Response(json.dumps(course), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CourseDetail(APIView):
    permission_classes = [IsHead]

    def get(self, request, course_id, format=None):
        try:
            course = get_course(course_id)
            return Response(json.dumps(course), status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            raise Http404
