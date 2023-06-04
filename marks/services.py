from .models import Mark


def update_mark(mark_id, mark_value, lesson_id):
    mark = Mark.objects.filter(id=mark_id).first()
    if mark:
        mark.mark_value = mark_value
        mark.lesson_id = lesson_id
        mark.save()
        return mark
    else:
        raise Exception('Mark not found')


def get_marks_by_course_and_date(course_id, year, month, day):
    marks = Mark.objects.filter(
        course_id=course_id, date__year=year, date__month=month, date__day=day)
    return marks


def create_mark(course_id, student_id, date, mark_value, lesson_id, assessment_id):
    mark = Mark.objects.create(course_id=course_id, student_id=student_id, date=date,
                               mark_value=mark_value, lesson_id=lesson_id, assessment_id=assessment_id)
    return mark
