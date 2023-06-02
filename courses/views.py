from django.shortcuts import render
from django.views.generic import DetailView, CreateView

from django.urls import reverse_lazy
from .models import Course
from .services import get_course, create_course

class CourseDetailView(DetailView):
    model = Course
    permission_classes = [IsTeacher]
    template_name = 'courses/course_detail.html'

    def get_object(self):
        course_id = self.kwargs.get("pk")
        return get_course(course_id)


class CourseCreateView(CreateView):
    model = Course
    fields = ['name', 'description', 'teacher']
    success_url = reverse_lazy('courses:course_detail')

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        description = form.cleaned_data.get('description')
        teacher = form.cleaned_data.get('teacher')
        create_course(name, description, teacher)
        return super().form_valid(form)
