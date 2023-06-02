from .models import Mark

def create_mark(student, class_, course, lesson_assessment, grade):
    mark = Mark.objects.create(student=student, class_id=class_, course=course, lesson_assessment=lesson_assessment, grade=grade)
    return mark

def get_mark(mark_id):
    return Mark.objects.get(id=mark_id)
