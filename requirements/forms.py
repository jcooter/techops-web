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

                        css_class='large-4'),
                    ),
                    Row(
                        Column(
                            'av_details',
                        css_class='large-6')
                    ),
                    Row(
                        Column(
                            InlineSwitchField('need_lighting'),
                        css_class='large-4')
                    ),
                    Row(
                        Column(
                            'lighting_details',
                        css_class='large-6')
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
                        css_class='large-4')
                    ),
                    Row(
                        Column(
                            'num_wired_drops',
                        css_class='large-2')
                    ),
                    Row(
                        Column(
                            'wired_drops_location',
                        css_class='large-4')
                    ),
                    Row(
                        Column(
                            'num_wireless_users',
                        css_class='large-2')
                    ),
                    Row(
                        Column(
                            'other_net_requirements',
                        css_class='large-6'),
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
                        css_class='large-4')
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
                        css_class='large-6'),
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
                        css_class='large-4')
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
                        css_class='large-6')
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
                        css_class='large-4')
                    ),
                    Row(
                        Column(
                            'num_phones',
                        css_class='large-2')
                    ),
                    Row(
                        Column(
                            'phone_location',
                        css_class='large-4')
                    ),
                    Row(
                        Column(
                            'other_phone_requirements',
                        css_class='large-6')
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
                        css_class='large-4')
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
                        css_class='large-6')
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
                        css_class='large-4')
                    ),
                    Row(
                        Column(
                            'num_rolls',
                        css_class='large-2')
                    ),
                    Row(
                        Column(
                            'other_tape_requirements',
                        css_class='large-6'),
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
                        css_class='large-6')
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
                            'feedback_rating',
                            'feedback_comments',
                        css_class='large-6')
                    ),
                )
            ),
        )
