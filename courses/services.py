from .models import Course, Class

def get_teacher_courses(teacher_id):
    courses = Course.objects.filter(teacher_id=teacher_id)
    return courses

def create_course(name, description, teacher):
    course = Course.objects.create(name=name, description=description, teacher=teacher)
    return course

def assign_class_to_course(course_id, class_id):
    course = Course.objects.get(id=course_id)
    class_ = Class.objects.get(id=class_id)
    course.classes.add(class_)
    course.save()
    return course

def get_course(course_id):
    return Course.objects.get(id=course_id)
