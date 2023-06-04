from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from django.views import View
from django.http import JsonResponse, HttpResponse

from StudentManagementAPI.permissions import IsHead
from .services import authenticate_user
from django.urls import reverse_lazy
from .models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import create_student, create_teacher, get_student, get_teacher
from django.http import Http404
import json


class StudentCreate(APIView):
    permission_classes = [IsHead]

    def post(self, request, format=None):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            student = create_student(name, email, password)
            return Response(json.dumps({"id": student.id, "name": student.name, "email": student.email}), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TeacherCreate(APIView):
    permission_classes = [IsHead]

    def post(self, request, format=None):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            teacher = create_teacher(name, email, password)
            return Response(json.dumps({"id": teacher.id, "name": teacher.name, "email": teacher.email}), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(APIView):
    permission_classes = [IsHead]

    def get(self, request, student_id, format=None):
        try:
            student = get_student(student_id)
            return Response(json.dumps({"id": student.id, "name": student.name, "email": student.email}), status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise Http404


class TeacherDetail(APIView):
    permission_classes = [IsHead]

    def get(self, request, teacher_id, format=None):
        try:
            teacher = get_teacher(teacher_id)
            return Response(json.dumps({"id": teacher.id, "name": teacher.name, "email": teacher.email}), status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise Http404


class LoginView(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        token = authenticate_user(username, password)
        if token:
            return JsonResponse(token)
        else:
            return HttpResponse("Invalid credentials", status=401)
