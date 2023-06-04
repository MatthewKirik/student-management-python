from django.urls import path
from .views import LoginView, StudentCreate, TeacherCreate, StudentDetail, TeacherDetail

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('users/students/', StudentCreate.as_view(), name='create_student'),
    path('users/teachers/', TeacherCreate.as_view(), name='create_teacher'),
    path('users/students/<int:student_id>',
         StudentDetail.as_view(), name='student_detail'),
    path('users/teachers/<int:teacher_id>',
         TeacherDetail.as_view(), name='teacher_detail'),
]
