from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (
        ('S', 'Student'),
        ('T', 'Teacher'),
        ('H', 'Head'),
    )
    role = models.CharField(max_length=1, choices=ROLES)

class Student(User):
    date_of_birth = models.DateField()
    address = models.TextField()
    contact_information = models.CharField(max_length=100)

class Teacher(User):
    contact_information = models.CharField(max_length=100)
