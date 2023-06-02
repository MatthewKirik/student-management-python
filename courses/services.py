from .models import Course

def create_course(name, description, teacher):
    course = Course.objects.create(name=name, description=description, teacher=teacher)
    return course

def get_course(course_id):
    return Course.objects.get(id=course_id)
