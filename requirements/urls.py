from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from . import views
from . import forms

urlpatterns = [
    url(r'^thisurl$', views.RequirementsWizard.as_view([
        forms.NewRequirementsForm1,
        forms.AVRequirementsForm,
        forms.NetworkRequirementsForm,
        forms.LaptopRequirementsForm,
        forms.PowerRequirementsForm,
        forms.PhoneRequirementsForm,
        forms.RadioRequirementsForm,
        forms.TapeRequirementsForm,
        forms.FeedbackRequirementsForm,
    ])),
    url(r'^$', views.index),
    url(r'^(?P<slug>[-\w]+)', views.event)
]