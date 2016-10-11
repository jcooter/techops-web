import datetime
from django.db import models
from django.conf import settings

from uber.models import Event

FEEDBACK_CHOICE = (
    ('very_poor', 'really sucks'),
    ('poor', 'sucks'),
    ('neutral', 'ain\'t bad'),
    ('good','is awesome'),
    ('very_good','is really awesome')
)

NETWORK_TYPE_CHOICE = (
    ('wifi', 'WiFi'),
    ('wired', 'Wired (Ethernet)'),
    ('both', 'Both')
)

def get_active_events():
    if settings.DEBUG:
        return {'epoch__gt': datetime.datetime.now()}
    else:
        return {
            'epoch__gt': datetime.datetime.now(),
            'type': 'prod'
        }

# Create your models here.
class RequirementsSubmission(models.Model):
    # Contact Info
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, limit_choices_to=get_active_events)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Request Submitted")
    department = models.CharField(max_length=32, verbose_name='Department')
    specific_department = models.CharField(max_length=32, blank=True, verbose_name='Specific Department')
    first_name = models.CharField(max_length=32, verbose_name='First Name')
    last_name = models.CharField(max_length=32, verbose_name='Last Name')
    contact_email = models.CharField(max_length=40, verbose_name='Contact E-Mail')

    # A/V Request
    create_av_request = models.BooleanField(default=False, verbose_name='Requires A/V')
    need_pa = models.BooleanField(default=False, verbose_name='Requires PA')
    need_wired_mic = models.BooleanField(default=False, verbose_name='Requires Wired Mic')
    need_wireless_mic = models.BooleanField(default=False, verbose_name='Requires Wireless Mic')
    need_laptop_input = models.BooleanField(default=False, verbose_name='Requires Laptop Input')
    need_other_audio = models.BooleanField(default=False, verbose_name='Other Audio Requirements')
    need_projector = models.BooleanField(default=False, verbose_name='Requires Projector')
    need_projection_screen = models.BooleanField(default=False, verbose_name='Requires Projection Screen')
    need_lcd_monitor = models.BooleanField(default=False, verbose_name='Requires LCD Monitor')
    need_tv = models.BooleanField(default=False, verbose_name='Requires Television')
    need_dvd_player = models.BooleanField(default=False, verbose_name='Requires Blu-ray/DVD Player')
    need_other_video = models.BooleanField(default=False, verbose_name='Other Video Requirements')
    av_details = models.TextField(blank=True, verbose_name='A/V Request Details')
    need_lighting = models.BooleanField(default=False, verbose_name='Requires Lighting')
    lighting_details = models.TextField(blank=True, verbose_name='Lighting Request Details')

    # Network Request
    create_network_request = models.BooleanField(default=False, verbose_name='Requires Network')
    network_type = models.CharField(max_length=24, blank=True, verbose_name='Connection Type', choices=NETWORK_TYPE_CHOICE)
    num_wired_drops = models.PositiveSmallIntegerField(blank=True, null=True, default=0, verbose_name='Wired Drop Count')
    wired_drops_location = models.CharField(max_length=64, blank=True, null=True, verbose_name='Wired Drop Location')
    num_wireless_users = models.PositiveSmallIntegerField(blank=True, null=True, default=0, verbose_name='Wireless User Count')
    other_net_requirements = models.TextField(blank=True, verbose_name='Other Network Requests')

    # Laptop Request
    create_laptop_request = models.BooleanField(default=False, verbose_name='Requires Laptops')
    num_laptops = models.PositiveSmallIntegerField(blank=True, null=True, default=0, verbose_name='Laptop Count')
    need_internet_access = models.BooleanField(default=False, verbose_name='Internet')
    need_uber_access = models.BooleanField(default=False, verbose_name='Uber')
    need_digital_signage = models.BooleanField(default=False, verbose_name=' Digital Signage')
    need_other_laptops = models.BooleanField(default=False, verbose_name='Other')
    need_custom_software = models.BooleanField(default=False, verbose_name='Laptops need custom software')
    other_laptop_requirements = models.TextField(blank=True, verbose_name='Other Laptop Requests')

    # Electrical Request
    create_power_request = models.BooleanField(default=False, verbose_name='Requires Power')
    num_power_strips = models.PositiveSmallIntegerField(blank=True, null=True, default=0, verbose_name='Power Strip Count')
    num_25ft_cords = models.PositiveSmallIntegerField(blank=True, null=True, default=0, verbose_name='25\' Extension Cord Count')
    num_50ft_cords = models.PositiveSmallIntegerField(blank=True, null=True, default=0, verbose_name='50\' Extension Cord Count')
    other_power_requirements = models.TextField(blank=True, verbose_name='Other Power Requests')

    # Phone Request
    create_phone_request = models.BooleanField(default=False, verbose_name='Requires IP Phones')
    num_phones = models.PositiveSmallIntegerField(blank=True, null=True, default=0, verbose_name='IP Phone Count')
    phone_location = models.CharField(max_length=64, blank=True, verbose_name='Phone Deployment Location')
    other_phone_requirements = models.TextField(blank=True, verbose_name='Other Phone Requests')

    # Radio Request
    create_radio_request = models.BooleanField(default=False, verbose_name='Requires Radios')
    num_radios = models.PositiveSmallIntegerField(blank=True, null=True, default=0, verbose_name='Radio Count')
    num_headsets = models.PositiveSmallIntegerField(blank=True, null=True, default=0, verbose_name='Headset Count')
    other_radio_requirements = models.TextField(blank=True, verbose_name='Other Radio Requests')
    
    # Tape Request
    create_tape_request = models.BooleanField(default=False, verbose_name='Requires Tape')
    num_rolls = models.PositiveSmallIntegerField(blank=True, null=True, default=0, verbose_name='Tape Roll Count')
    other_tape_requirements = models.TextField(blank=True, verbose_name='Other Tape Requests')

    other_request = models.TextField(blank=True, verbose_name='Other Requests')
    feedback_rating = models.CharField(max_length=24, blank=True, verbose_name='Feedback Rating',choices=FEEDBACK_CHOICE)
    feedback_comments = models.TextField(blank=True, verbose_name='Comments')
