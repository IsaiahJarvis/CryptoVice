from django.shortcuts import render
from .forms import BaseUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUpView(CreateView):
    form_class = BaseUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
