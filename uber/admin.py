from django.contrib import admin

from .models import Event

class UberEventAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'api_url')
    def get_readonly_fields(self, request, obj=None):
        return [
            'api_version',
            'name',
            'org_name',
            'year',
            'epoch',
            'venue',
            'venue_address',
            'at_the_con',
            'post_con'
        ]

# Register your models here.
admin.site.register(Event,UberEventAdmin)