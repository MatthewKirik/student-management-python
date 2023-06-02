from rest_framework.permissions import BasePermission

class IsHead(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'head'

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'teacher'