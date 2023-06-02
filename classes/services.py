from .models import Class

def create_class(course, teacher):
    class_ = Class.objects.create(course=course, teacher=teacher)
    return class_

def get_class(class_id):
    return Class.objects.get(id=class_id)
