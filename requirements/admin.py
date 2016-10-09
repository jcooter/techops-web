from django.contrib import admin
from .models import RequirementsSubmission

class RequirementsSubmissionAdmin(admin.ModelAdmin):
    list_display = ('department', 'first_name', 'last_name', 'contact_email', 'create_av_request', 'create_network_request', 'create_laptop_request', 'create_power_request', 'create_phone_request', 'create_radio_request', 'create_tape_request')

admin.site.register(RequirementsSubmission, RequirementsSubmissionAdmin)
# Register your models here.
