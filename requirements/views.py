from pprint import pprint

from django.shortcuts import render
from django import forms
from django.views.generic import FormView
from rpctools.jsonrpc import ServerProxy

from .forms import RequirementsForm
from uber.models import Event

def index(request):
    if request.method == 'POST':
        form = RequirementsForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, 'thanks.html')
    else:
        form = RequirementsForm()
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