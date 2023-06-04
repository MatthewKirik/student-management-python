from django.db import models
from users.models import User
from courses.models import Course


class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'T'})
