from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from .views import RequirementsFormView

urlpatterns = [
    url(r'^$', RequirementsFormView.as_view()),
]