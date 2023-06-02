from django.db import models
from users.models import Student
from classes.models import Class
from courses.models import Course

class Mark(models.Model):
    mark_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson_assessment = models.CharField(max_length=200)
    grade = models.CharField(max_length=3)
