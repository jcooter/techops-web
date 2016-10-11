from django.contrib import admin

from .models import Event

class UberEventAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'api_url')

# Register your models here.
admin.site.register(Event,UberEventAdmin)