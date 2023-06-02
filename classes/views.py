from django.shortcuts import render
from django.views.generic import DetailView, CreateView

from django.urls import reverse_lazy
from .models import Class
from .services import get_class, create_class

class ClassDetailView(DetailView):
    model = Class
    template_name = 'classes/class_detail.html'

    def get_object(self):
        class_id = self.kwargs.get("pk")
        return get_class(class_id)


class ClassCreateView(CreateView):
    model = Class
    fields = ['course', 'teacher']
    success_url = reverse_lazy('classes:class_detail')

    def form_valid(self, form):
        course = form.cleaned_data.get('course')
        teacher = form.cleaned_data.get('teacher')
        create_class(course, teacher)
        return super().form_valid(form)
