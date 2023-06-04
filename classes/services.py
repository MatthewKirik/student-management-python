import StudentManagementAPI
from .models import Class


def create_class(name):
    class_ = Class.objects.create(name=name)
    return class_


def assign_students_to_class(class_id, student_ids):
    class_ = Class.objects.get(id=class_id)
    students = StudentManagementAPI.objects.filter(id__in=student_ids)
    class_.students.add(*students)
    class_.save()
    return class_


def get_teacher_course_classes(teacher_id, course_id):
    classes = Class.objects.filter(
        courses__teacher_id=teacher_id, courses__id=course_id)
    return classes


def get_class(class_id):
    return Class.objects.get(id=class_id)
