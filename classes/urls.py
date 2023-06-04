from django.urls import path
from .views import ClassCreate, StudentsToClassAssignment, TeacherCourseClassesList, ClassDetail

urlpatterns = [
    path('classes/', ClassCreate.as_view(), name='create_class'),
    path('classes/<int:class_id>/students',
         StudentsToClassAssignment.as_view(), name='assign_students_to_class'),
    path('teachers/<int:teacher_id>/courses/<int:course_id>/classes',
         TeacherCourseClassesList.as_view(), name='get_teacher_course_classes'),
    path('classes/<int:class_id>', ClassDetail.as_view(), name='class_detail'),
]
