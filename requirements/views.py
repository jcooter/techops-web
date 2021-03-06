from pprint import pprint

import datetime
from django.conf import settings
from django.shortcuts import render
from django import forms
from django.views.generic import FormView
from formtools.wizard.views import SessionWizardView
from rpctools.jsonrpc import ServerProxy

from .forms import RequirementsForm
from uber.models import Event

class RequirementsWizard(SessionWizardView):
    def get_template_names(self):
        return 'form.html'

    def done(self, form_list, **kwargs):
        return render(request, 'thanks.html')

def index(request):
    if request.method == 'POST':
        form = RequirementsForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, 'thanks.html')
    else:
        form = RequirementsForm()
        if settings.DEBUG:
            events = Event.objects.filter(epoch__gt=datetime.datetime.now())
        else:
            events = Event.objects.filter(epoch__gt=datetime.datetime.now()).filter(type='prod')

        if events:
            uber = ServerProxy(
                uri=events[0].api_url,
                cert_file=events[0].ssl_client_cert.name,
                key_file=events[0].ssl_client_key.name
            )
            form.fields['department'].widget = forms.widgets.Select(choices=uber.dept.list().items())
    return render(request, 'form.html', {'form': form})

def event(request, slug):
    if request.method == 'POST':
        form = RequirementsForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, 'thanks.html')
    else:
        form = RequirementsForm()

        event = Event.objects.get(slug=slug)
        uber = ServerProxy(
            uri=event.api_url,
            cert_file=event.ssl_client_cert.name,
            key_file=event.ssl_client_key.name
        )

        if (event.slug, event.__unicode__()) not in form.fields['event'].widget.choices:
            choices = ()
            for choice in form.fields['event'].choices:
                choices += (choice, )
            choices += (( event.slug, event.__unicode__() ), )
            form.fields['event'].choices = choices
            if len(choices) == 1:
                form.fields['event'].disabled = True
            else:
                form.fields['event'].disabled = False
        form.fields['event'].initial = event.slug
        form.fields['department'].choices = uber.dept.list().items()
        form.fields['department'].widget = forms.widgets.Select(choices=uber.dept.list().items())
    return render(request, 'form.html', {'form': form})