from django.shortcuts import render
from django import forms
from django.views.generic import FormView
from .forms import RequirementsForm


class RequirementsFormView(FormView):
    template_name = "form.html"
    form_class = RequirementsForm