from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML, Fieldset
from crispy_forms_foundation.layout import TabHolder, TabItem, Row, Column, SwitchField, InlineSwitchField

from .models import RequirementsSubmission

class RequirementsForm(forms.ModelForm):
    class Meta:
        model = RequirementsSubmission
        exclude = []

    def __init__(self, *args, **kwargs):
        super(RequirementsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-requirementsForm'
        self.helper.form_class = 'requirementsForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_requirements'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            TabHolder(
                TabItem('General Info',
                    Row(
                        Column(
                            Row(
                                Column('department', css_class='large-12'),
                            ),
                            Row(
                                Column('specific_department', css_class='large-12'),
                            ),
                            Row(
                                Column('first_name', css_class='large-6'),
                                Column('last_name', css_class='large-6'),
                            ),
                            Row(
                                Column('contact_email', css_class='large-12')
                            ),
                        css_class='large-4'),
                    ),
                ),
                TabItem('A/V Requests',
                    Row(
                        Column(
                            HTML("<h3>A/V Requirements</h3>"),
                            HTML("<p>NOTE: Rental fees for some of this equipment may come out of your department's budget</p>"),
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
                            'av_details',
                            Fieldset(
                                'Lighting Equipment',
                                'need_lighting',
                                'lighting_details'
                            ),
                        css_class='large-4'),
                    ),
                ),
                TabItem('Network Requests',
                    Row(
                        Column(
                            HTML("<h3>Network Access Requirements</h3>"),
                            'create_network_request'
                            'network_type',
                            'num_wired_drops',
                            'wired_drops_location',
                            'num_wireless_users',
                            'other_net_requirements',
                        css_class='large-4'),
                    ),
                ),
                TabItem('Laptop Requests',
                    Row(
                        Column(
                            HTML('<h3>Laptop Requirements</h3>'),
                            HTML('<p>Please note, by default laptops DO NOT come with Windows.  Windows licenses are expensive.  If you need Windows laptops, indicate that in the "Other" box below and include justification.'),
                            'create_laptop_request',
                            'num_laptops',
                            Fieldset(
                                'I need laptops to do the following',
                                'need_internet_access',
                                'need_uber_access',
                                'need_digital_signage',
                                'need_other_laptops',
                            ),
                            'need_custom_software',
                            'other_laptop_requirements',
                        css_class='large-4'),
                    ),
                ),
                TabItem('Electrical Requests',
                    Row(
                        Column(
                            HTML('<h3>Electrical Requirements</h3>'),
                            HTML('<p>If you do not need any of a specific item, please enter 0'),
                            'create_power_request',
                            'num_power_strips',
                            'num_25ft_cords',
                            'num_50ft_cords',
                            'other_power_requirements',
                        css_class='large-4')
                    )
                ),
                TabItem('Misc. Requests',
                    Row(
                        Column(
                            HTML('<h3>IP Phone Requests</h3>'),
                            HTML('<p>These hard-wired phones can be used to call other departments</p>'),
                            'create_phone_request',
                            'num_phones',
                            'phone_location',
                            'other_phone_requirements',
                        css_class='large-4')
                    ),
                    Row(
                        Column(
                            HTML('<h3>Radio Requests</h3>'),
                            HTML('<p>NOTE: Radio rental fees may come out of your department\'s budget.  Please consider if you actually need these items or not.'),
                            'create_radio_request',
                            'num_radios',
                            'num_headsets',
                            'other_radio_requirements',
                        css_class='large-4')
                    ),
                    Row(
                        Column(
                            HTML('<h3>Gaff Tape Requests</h3>'),
                            HTML('<p>NOTE: Tape costs may come out of your department\'s budget.  Please consider the cost when you request tape.'),
                            'create_tape_request',
                            'num_rolls',
                            'other_tape_requirements',
                        css_class='large-4'),
                    ),
                    Row(
                        Column(
                            HTML('<h3>Other Requests</h3>'),
                            HTML('<p>If you wanted to ask for something and didn\'t see a place to ask, now is your chance!'),
                            'other_request',
                        css_class='large-4')
                    )
                ),
                TabItem('Feedback',
                    Row(
                        Column(
                            HTML('<h3>Feedback on this form</h3>'),
                            HTML('<p>We welcome any input you might have on this form or our general process for handling tech requests.</p>'),
                            'feedback_rating',
                            'feedback_comments',
                        css_class='large-4')
                    )

                )
            ),
        )