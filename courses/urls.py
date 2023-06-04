from django.urls import path
from .views import TeacherCoursesList, CourseCreate, ClassToCourseAssignment, CourseDetail

urlpatterns = [
    path('teachers/<int:teacher_id>/courses',
         TeacherCoursesList.as_view(), name='get_teacher_courses'),
    path('courses/', CourseCreate.as_view(), name='create_course'),
    path('courses/<int:course_id>/classes/<int:class_id>',
         ClassToCourseAssignment.as_view(), name='assign_class_to_course'),
    path('courses/<int:course_id>', CourseDetail.as_view(), name='course_detail'),
]
