from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


def create_student(name, email, password):
    student = User.objects.create(
        name=name, email=email, password=password, role='student')
    return student


def create_teacher(name, email, password):
    teacher = User.objects.create(
        name=name, email=email, password=password, role='teacher')
    return teacher


def get_student(student_id):
    return User.objects.get(id=student_id, role='student')


def get_teacher(teacher_id):
    return User.objects.get(id=teacher_id, role='teacher')


def authenticate_user(username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    else:
        return None
