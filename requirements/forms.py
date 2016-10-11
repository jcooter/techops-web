from pprint import pprint

import datetime
from django import forms
from django.forms import RadioSelect
from django.forms.widgets import RadioFieldRenderer, Select, HiddenInput
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML, Fieldset
from crispy_forms_foundation.layout import TabHolder, TabItem, Row, Column, SwitchField, InlineSwitchField
from rpctools.jsonrpc import ServerProxy

from .models import RequirementsSubmission
from uber.models import Event

YES_NO_CHOICE = (
    ( True, _('Yes')),
    ( False, _('No'))
)

class FieldsetRadioFieldRenderer(RadioFieldRenderer):
    outer_html = '{content}'
    inner_html = '<div class="holder">{choice_value}{sub_widgets}</div>'

class InlineRadioFieldRenderer(RadioFieldRenderer):
    outer_html = '<div class="row"{id_attr}>{content}</div>'
    inner_html = '<div class="large-{size} columns end">{choice_value}{sub_widgets}</div>'

    def render(self):
        id_ = self.attrs.get('id')
        output = []
        size = 12 / len(self.choices)
        for i, choice in enumerate(self.choices):
            choice_value, choice_label = choice
            if isinstance(choice_label, (tuple, list)):
                attrs_plus = self.attrs.copy()
                if id_:
                    attrs_plus['id'] += '_{}'.format(i)
                sub_ul_renderer = self.__class__(
                    name=self.name,
                    value=self.value,
                    attrs=attrs_plus,
                    choices=choice_label
                )
                sub_ul_renderer.choice_input_class = self.choice_input_class
                output.append(format_html(
                    self.inner_html, choice_value=choice_value,
                    size=size, sub_widgets=sub_ul_renderer.render(),
                ))
            else:
                w = self.choice_input_class(self.name, self.value, self.attrs.copy(), choice, i)
                output.append(format_html(self.inner_html, choice_value=force_text(w), size=size, sub_widgets=''))
        return format_html(
            self.outer_html,
            id_attr=format_html(' id="{}"', id_) if id_ else '',
            content=mark_safe('\n'.join(output)),
        )

class RequirementsForm(forms.ModelForm):
    class Meta:
        model = RequirementsSubmission
        exclude = []

        _DEPARTMENT_CHOICE = []

        @property
        def DEPARTMENT_CHOICE(self):
            return self._DEPARTMENT_CHOICE

        @DEPARTMENT_CHOICE.setter
        def DEPARTMENT_CHOICE(self, value):
            self._DEPARTMENT_CHOICE = value

        if not settings.DEBUG:
            events = Event.objects.filter(epoch__gt=datetime.datetime.now())
        else:
            events = Event.objects.filter(epoch__gt=datetime.datetime.now()).filter(type='prod')

        if events:
            uber = ServerProxy(
                uri=events[0].api_url,
                cert_file=events[0].ssl_client_cert.name,
                key_file=events[0].ssl_client_key.name
            )
            _DEPARTMENT_CHOICE = uber.dept.list().items()

        widgets = {
            'need_custom_software': RadioSelect(
                choices=YES_NO_CHOICE,
                renderer=InlineRadioFieldRenderer),
            'feedback_rating': RadioSelect(renderer=FieldsetRadioFieldRenderer),
            'network_type': RadioSelect(renderer=InlineRadioFieldRenderer),
            'department': Select(choices=_DEPARTMENT_CHOICE)
        }
        labels = {
            'create_av_request': _('Our department needs A/V Equipment'),

            'need_pa': _('PA Systems / Speakers'),
            'need_wired_mic': _('Wired Microphones'),
            'need_wireless_mic': _('Wireless Microphones'),
            'need_laptop_input': _('Laptop / Phone Inputs'),
            'need_other_audio': _('Other'),

            'need_projector': _('Projectors'),
            'need_projection_screen': _('Projection Screens'),
            'need_lcd_monitor': _('LCD Computer Monitors'),
            'need_tv': _('Televisions'),
            'need_dvd_player': _('DVD/Blu-ray Players'),
            'need_other_video': _('Other'),

            'av_details': _('Details'),

            'need_lighting': _('Our department needs Lighting Equipment'),
            'lighting_details': _('Details'),

            'create_network_request': _('Our department needs Network access'),
            'network_type': _('What type of network connection do you need?'),
            'num_wired_drops': _('Approximately how many wired drops do you need?'),
            'wired_drops_location': _('What room(s) do you need wired drops in?'),
            'num_wireless_users': _('Approximately how many users will need wireless access?'),
            'other_net_requirements': _('Other requirements?'),

            'create_laptop_request': _('Our department needs laptops'),
            'num_laptops': _('How many laptops do you need?'),

            'need_internet_access': _('Access the Internet'),
            'need_uber_access': _('Access Uber/RAMS'),
            'need_digital_signage': _('Run digital signage'),
            'need_other_laptops': _('Other'),

            'need_custom_software': _('I need to install software on our laptops'),
            'other_laptop_requirements': _('Other requirements?'),

            'create_power_request': _('Our department needs extension cords, power strips, etc.'),
            'num_power_strips': _('How many power strips do you need?'),
            'num_25ft_cords': _('How many 25 foot extension cords do you need?'),
            'num_50ft_cords': _('How many 50 foot extension cords do you need?'),
            'other_power_requirements': _('Other requirements?'),

            'create_phone_request': _('Our department needs IP Phones'),
            'num_phones': _('How many phones?'),
            'phone_location': _('Which room(s) do you need these phones?'),
            'other_phone_requirements': _('Special Requirements?'),

            'create_radio_request': _('Our department needs radios'),
            'num_radios': _('How many radios?'),
            'num_headsets': _('How many headsets?'),
            'other_radio_requirements': _('Special Requirements?'),

            'create_tape_request': _('Our department needs gaff tape'),
            'num_rolls': _('How many rolls?'),
            'other_tape_requirements': _('Special Requirements'),

            'other_request': _(''),

            'feedback_rating': _(''),
            'feedback_comments': _('Comments / Suggestions')
        }

    def __init__(self, *args, **kwargs):
        super(RequirementsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-requirementsForm'
        self.helper.form_class = 'requirementsForm'
        self.helper.form_method = 'post'
        #self.helper.form_action = 'submit_requirements'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.fields['event'].empty_label=None
        if len(self.fields['event'].choices) == 1:
            for choice in self.fields['event'].choices:
                self.fields['event'].disabled=True
                self.fields['event'].initial=choice[0]
        self.fields['feedback_rating'].choices = self.fields['feedback_rating'].choices[1:]
        self.fields['network_type'].choices = self.fields['network_type'].choices[1:]
        self.helper.layout = Layout(
            TabHolder(
                TabItem('General Info',
                    Row(
                        Column(
                            Row(
                                Column('event', css_class='large-12'),
                            ),
                            Row(
                                Column('department', css_class='large-12'),
                            ),
                            Row(
                                Column('specific_department', css_class='large-12'),
                            ),
                            Row(
                                Column('first_name', css_class='large-5'),
                                Column('last_name', css_class='large-7'),
                            ),
                            Row(
                                Column('contact_email', css_class='large-12')
                            ),
                        css_class='large-4'),
                    ),
                ),
                TabItem('A/V',
                    Row(
                        Column(
                            HTML("<h3>A/V Requirements</h3>"),
                            HTML("<p>NOTE: Rental fees for some of this equipment may come out of your department's budget</p>"),
                        css_class='large-12')
                    ),
                    Row(
                        Column(
                            InlineSwitchField('create_av_request'),
                            Fieldset(
                                'Audio Equipment',
                                'need_pa',
                                'need_wired_mic',
                                'need_wireless_mic',
                                'need_laptop_input',
                                'need_other_audio',
                            ),
                            Fieldset(
                                'Video Equipment',
                                'need_projector',
                                'need_projection_screen',
                                'need_lcd_monitor',
                                'need_tv',
                                'need_dvd_player',
                                'need_other_video',
                            ),

                        css_class='large-6'),
                    ),
                    Row(
                        Column(
                            'av_details',
                        css_class='large-8')
                    ),
                    Row(
                        Column(
                            InlineSwitchField('need_lighting'),
                        css_class='large-6')
                    ),
                    Row(
                        Column(
                            'lighting_details',
                        css_class='large-8')
                    ),
                ),
                TabItem('Network',
                    Row(
                        Column(
                            HTML("<h3>Network Access Requirements</h3>"),
                        css_class='large-12')
                    ),
                    Row(
                        Column(
                            InlineSwitchField('create_network_request'),
                            'network_type',
                        css_class='large-6')
                    ),
                    Row(
                        Column(
                            'num_wired_drops',
                        css_class='large-2')
                    ),
                    Row(
                        Column(
                            'wired_drops_location',
                        css_class='large-6')
                    ),
                    Row(
                        Column(
                            'num_wireless_users',
                        css_class='large-2')
                    ),
                    Row(
                        Column(
                            'other_net_requirements',
                        css_class='large-8'),
                    ),
                ),

                TabItem('Laptops',
                    Row(
                        Column(
                            HTML('<h3>Laptop Requirements</h3>'),
                            HTML('<p>Please note, by default laptops DO NOT come with Windows.  Windows licenses are expensive.  If you need Windows laptops, indicate that in the "Other" box below and include justification.'),
                        css_class='large-12')
                    ),
                    Row(
                        Column(
                            InlineSwitchField('create_laptop_request'),
                        css_class='large-6')
                    ),
                    Row(
                        Column(
                            'num_laptops',
                        css_class='large-2')
                    ),
                    Row(
                        Column(
                            Fieldset(
                                'I need laptops to do the following',
                                'need_internet_access',
                                'need_uber_access',
                                'need_digital_signage',
                                'need_other_laptops',
                            ),
                            'need_custom_software',
                        css_class='large-4'),
                    ),
                    Row(
                        Column(
                            'other_laptop_requirements',
                        css_class='large-8'),
                    ),
                ),
                TabItem('Electrical',
                    Row(
                        Column(
                            HTML('<h3>Electrical Requirements</h3>'),
                            HTML('<p>If you do not need any of a specific item, please enter 0'),
                        css_class='large-12')
                    ),
                    Row(
                        Column(
                            InlineSwitchField('create_power_request'),
                        css_class='large-7')
                    ),
                    Row(
                        Column(
                            'num_power_strips',
                            'num_25ft_cords',
                            'num_50ft_cords',
                        css_class='large-2')
                    ),
                    Row(
                        Column(
                            'other_power_requirements',
                        css_class='large-8')
                    )
                ),
                TabItem('Misc. Requests',
                    Row(
                        Column(
                            HTML('<h3>IP Phone Requests</h3>'),
                            HTML('<p>These hard-wired phones can be used to call other departments</p>'),
                        css_class='large-12')
                    ),
                    Row(
                        Column(
                            InlineSwitchField('create_phone_request'),
                        css_class='large-6')
                    ),
                    Row(
                        Column(
                            'num_phones',
                        css_class='large-2')
                    ),
                    Row(
                        Column(
                            'phone_location',
                        css_class='large-6')
                    ),
                    Row(
                        Column(
                            'other_phone_requirements',
                        css_class='large-8')
                    ),
                    Row(
                        Column(
                            HTML('<h3>Radio Requests</h3>'),
                            HTML('<p>NOTE: Radio rental fees may come out of your department\'s budget.  Please consider if you actually need these items or not.'),
                        css_class='large-12')
                    ),
                    Row(
                        Column(
                            InlineSwitchField('create_radio_request'),
                        css_class='large-6')
                    ),
                    Row(
                        Column(
                            'num_radios',
                            'num_headsets',
                        css_class='large-2')
                    ),
                    Row(
                        Column(
                            'other_radio_requirements',
                        css_class='large-8')
                    ),
                    Row(
                        Column(
                            HTML('<h3>Gaff Tape Requests</h3>'),
                            HTML('<p>NOTE: Tape costs may come out of your department\'s budget.  Please consider the cost when you request tape.'),
                        css_class='large-12')
                    ),
                    Row(
                        Column(
                            InlineSwitchField('create_tape_request'),
                        css_class='large-6')
                    ),
                    Row(
                        Column(
                            'num_rolls',
                        css_class='large-2')
                    ),
                    Row(
                        Column(
                            'other_tape_requirements',
                        css_class='large-8'),
                    ),
                    Row(
                        Column(
                            HTML('<h3>Other Requests</h3>'),
                            HTML('<p>If you wanted to ask for something and didn\'t see a place to ask, now is your chance!'),
                        css_class='large-12')
                    ),
                    Row(
                        Column(
                            'other_request',
                        css_class='large-8')
                    )
                ),
                TabItem('Feedback',
                    Row(
                        Column(
                            HTML('<h3>Feedback on this form</h3>'),
                            HTML('<p>We welcome any input you might have on this form or our general process for handling tech requests.</p>'),
                        css_class='large-12')
                    ),
                    Row(
                        Column(
                            Fieldset(
                                'I think this form:',
                                'feedback_rating'
                            ),
                            'feedback_comments',
                        css_class='large-8')
                    ),
                )
            ),
        )
