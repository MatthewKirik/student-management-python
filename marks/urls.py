from django.urls import path
from .views import MarkCreate, MarkUpdate, MarksByCourseAndDate

urlpatterns = [
    path('marks/<int:mark_id>', MarkUpdate.as_view(), name='update_mark'),
    path('courses/<int:course_id>/marks/<int:year>/<int:month>/<int:day>',
         MarksByCourseAndDate.as_view(), name='get_marks_by_course_and_date'),
    path('marks/', MarkCreate.as_view(), name='create_mark'),
]
