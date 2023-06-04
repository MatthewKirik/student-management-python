from pyclbr import Class
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from StudentManagementAPI.permissions import IsHead, IsTeacher
from .services import create_class, assign_students_to_class, get_teacher_course_classes, get_class
from django.http import Http404
import json

class ClassCreate(APIView):
    permission_classes = [IsHead]

    def post(self, request, format=None):
        name = request.data.get('name')
        try:
            class_ = create_class(name)
            return Response(json.dumps({"id": class_.id, "name": class_.name}), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentsToClassAssignment(APIView):
    permission_classes = [IsHead]

    def post(self, request, class_id, format=None):
        student_ids = request.data.get('student_ids')
        try:
            class_ = assign_students_to_class(class_id, student_ids)
            students = [{"id": student.id, "name": student.name} for student in class_.students.all()]
            return Response(json.dumps({"id": class_.id, "name": class_.name, "students": students}), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TeacherCourseClassesList(APIView):
    permission_classes = [IsTeacher]

    def get(self, request, teacher_id, course_id, format=None):
        classes = get_teacher_course_classes(teacher_id, course_id)
        classes_data = [{"id": class_.id, "name": class_.name} for class_ in classes]
        return Response(json.dumps(classes_data), status=status.HTTP_200_OK)


class ClassDetail(APIView):
    permission_classes = [IsHead]

    def get(self, request, class_id, format=None):
        try:
            class_ = get_class(class_id)
            students = [{"id": student.id, "name": student.name} for student in class_.students.all()]
            return Response(json.dumps({"id": class_.id, "name": class_.name, "students": students}), status=status.HTTP_200_OK)
        except Class.DoesNotExist:
            raise Http404
