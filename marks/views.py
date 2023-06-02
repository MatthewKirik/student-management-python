from django.shortcuts import render
from django.views.generic import DetailView, CreateView

from django.urls import reverse_lazy

from StudentManagementAPI.permissions import IsTeacher
from .models import Mark
from .services import get_mark, create_mark

class MarkDetailView(DetailView):
    model = Mark
    template_name = 'marks/mark_detail.html'
    permission_classes = [IsTeacher]

    def get_object(self):
        mark_id = self.kwargs.get("pk")
        return get_mark(mark_id)


class MarkCreateView(CreateView):
    model = Mark
    fields = ['student', 'class_id', 'course', 'lesson_assessment', 'grade']
    success_url = reverse_lazy('marks:mark_detail')
    permission_classes = [IsTeacher]

    def form_valid(self, form):
        student = form.cleaned_data.get('student')
        class_ = form.cleaned_data.get('class_id')
        course = form.cleaned_data.get('course')
        lesson_assessment = form.cleaned_data.get('lesson_assessment')
        grade = form.cleaned_data.get('grade')
        create_mark(student, class_, course, lesson_assessment, grade)
        return super().form_valid(form)
