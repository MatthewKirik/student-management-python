from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from django.views import View
from django.http import JsonResponse, HttpResponse
from .services import authenticate_user
from django.urls import reverse_lazy
from .models import User
from .services import get_user, create_user

class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'

    def get_object(self):
        user_id = self.kwargs.get("pk")
        return get_user(user_id)


class UserCreateView(CreateView):
    model = User
    fields = ['username', 'password', 'role']
    success_url = reverse_lazy('users:user_detail')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        role = form.cleaned_data.get('role')
        create_user(username, password, role)
        return super().form_valid(form)

class LoginView(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        token = authenticate_user(username, password)
        if token:
            return JsonResponse(token)
        else:
            return HttpResponse("Invalid credentials", status=401)
