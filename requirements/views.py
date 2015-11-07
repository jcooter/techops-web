from django.shortcuts import render
from django import forms
from django.contrib.auth import authenticate
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import loader, Context
import simplejson
from django.views.decorators.csrf import csrf_exempt
import logging
from .models import RequirementsSubmission
import puka
from jira import JIRA

STATUS_OK = 200

STATUS_ERROR = 400
STATUS_ERROR_NOT_FOUND = 404
STATUS_ERROR_PERMISSIONS = 403
STATUS_ERROR_BADMETHOD = 405

amqp_producer = puka.Client('amqp://localhost/')
connect_promise = amqp_producer.connect()
amqp_producer.wait(connect_promise)

exchange_promise = amqp_producer.exchange_declare(exchange='magfest.techops.notifications', type='fanout')
amqp_producer.wait(exchange_promise)

jira = JIRA('https://jira.magfest.net')

@csrf_exempt
def api(request, method):
    if request.method != 'POST':
        return api_return(STATUS_ERROR_BADMETHOD)

    api = API(request)
    if hasattr(api, 'api_public_%s' % method):
        return getattr(api, 'api_public_%s' % method)()

    return api_return(STATUS_ERROR)


def api_return(status, text='', json=False):
    content_type = 'text/plain'
    if status == STATUS_OK and json:
        content_type = 'text/json'

    if text is None:
        if status == STATUS_ERROR:
            text = 'Error'
        elif status == STATUS_ERROR_NOT_FOUND:
            text = 'Resource Not Found'
        elif status == STATUS_ERROR_PERMISSIONS:
            text = 'Invalid username or password'
        elif status == STATUS_ERROR_BADMETHOD:
            text = 'Invalid request method'
        elif status == STATUS_OK:
            text = 'OK'

    r = HttpResponse(status=status, content=text, content_type=content_type)

    if status == STATUS_ERROR_BADMETHOD:
        r.Allow = 'POST'

    return r


class API:
    def __init__(self, request):
        self.request = request
        self.logger = logging.getLogger(__name__)

    def api_public_wufoo(self):
        if self.request.POST.get('HandshakeKey') == 'qz6jbuGSzTEHYx':
            submission = RequirementsSubmission()
            # Page 1 - Contact Info 
            submission.department = self.request.POST.get('Field1')
            description = 'Department:  %s\n' % (submission.department)
            submission.specific_department = self.request.POST.get('Field2')
            description += 'Specific Department:  %s\n' % (submission.specific_department)
            submission.first_name = self.request.POST.get('Field9')
            submission.last_name = self.request.POST.get('Field10')
            description += 'Contact Name:  %s %s\n' % (submission.first_name, submission.last_name)
            submission.contact_email = self.request.POST.get('Field11')
            description += 'Contact Email:  %s\n' % (submission.contact_email)

            # Page 2 - A/V Request
            if self.request.POST.get('Field215') == 'Yes':
                submission.create_av_request = True
                submission.need_pa = bool(self.request.POST.get('Field115'))
                av_description = description + 'Need PA: %s\n' % (submission.need_pa)
                submission.need_wired_mic = bool(self.request.POST.get('Field116'))
                av_description += 'Need Wired Mic: %s\n' % (submission.need_wired_mic)
                submission.need_wireless_mic = bool(self.request.POST.get('Field117'))
                av_description += 'Need Wireless Mic: %s\n' % (submission.need_wireless_mic)
                submission.need_laptop_input = bool(self.request.POST.get('Field118'))
                av_description += 'Need Laptop Input: %s\n' % (submission.need_laptop_input)
                submission.need_other_audio = bool(self.request.POST.get('Field119'))
                av_description += 'Need Other Audio: %s\n' % (submission.need_other_audio)
                submission.need_projector = bool(self.request.POST.get('Field217'))
                av_description += 'Need Projector: %s\n' % (submission.need_projector)
                submission.need_projection_screen = bool(self.request.POST.get('Field218'))
                av_description += 'Need Screen: %s\n' % (submission.need_projection_screen)
                submission.need_lcd_monitor = bool(self.request.POST.get('Field219'))
                av_description += 'Need LCD Monitor: %s\n' % (submission.need_lcd_monitor)
                submission.need_tv = bool(self.request.POST.get('Field220'))
                av_description += 'Need Television: %s\n' % (submission.need_tv)
                submission.need_dvd_player = bool(self.request.POST.get('Field221'))
                av_description += 'Need DVD/Blu-ray Player: %s\n' % (submission.need_dvd_player)
                submission.need_other_video = bool(self.request.POST.get('Field222'))
                av_description += 'Need Other Video: %s\n' % (submission.need_other_video)
                submission.av_details = self.request.POST.get('Field317')
                av_description += 'Details:\n%s\n' % (submission.av_details)
                if self.request.POST.get('Field319') == 'I want to request some lighting equipment':
                    submission.need_lighting = True
                    av_description += 'Lighting Requested: Yes\n'
                    submission.lighting_details = self.request.POST.get('Field320')
                    av_description += 'Details:\n%s\n' % (submission.lighting_details)
                else:
                    submission.need_lighting = False
                    av_description += 'Lighting Requested: No\n'
                    submission.lighting_details = ""
            else:
                submission.create_av_request = False

            # Page 3 - Network Request
            if self.request.POST.get('Field326') == 'Yes':
                network_description = description
                submission.create_network_request = True
                submission.network_type = self.request.POST.get('Field333')
                network_description += 'Network Type: %s\n' % (submission.network_type)
                if self.request.POST.get('Field335'):
                    submission.num_wired_drops = int(self.request.POST.get('Field335'))
                    network_description += 'Number of Wired Drops: %d\n' % (submission.num_wired_drops)
                    submission.wired_drops_location = self.request.POST.get('Field334')
                    network_description += 'Wired Drop Location: %s\n' % (submission.wired_drops_location)
                if self.request.POST.get('Field336'):
                    submission.num_wireless_users = int(self.request.POST.get('Field336'))
                    network_description += 'Number of Wireless Users: %d\n' % (submission.num_wireless_users)
                submission.other_net_requirements = self.request.POST.get('Field337')
                network_description += 'Other Requirements: %s\n' % (submission.other_net_requirements)
            else:
                submission.create_network_request = False
                network_description = description
            
            # Page 4 - Laptop Request
            if self.request.POST.get('Field351') == 'Yes':
                laptop_description = description
                submission.create_laptop_request = True
                if self.request.POST.get('Field354'):
                    submission.num_laptops = int(self.request.POST.get('Field354'))
                    laptop_description += 'Number of Laptops: %d\n' % (submission.num_laptops)
                submission.need_internet_access = bool(self.request.POST.get('Field355'))
                laptop_description += 'Need Internet Access: %s\n' % (submission.need_internet_access)
                submission.need_uber_access = bool(self.request.POST.get('Field356'))
                laptop_description += 'Need Uber Access: %s\n' % (submission.need_uber_access)
                submission.need_digital_signage = bool(self.request.POST.get('Field357'))
                laptop_description += 'Need Digital Signage: %s\n' % (submission.need_digital_signage)
                submission.need_other_laptops = bool(self.request.POST.get('Field358'))
                laptop_description += 'Other: %s\n' % (submission.need_other_laptops)
                if self.request.POST.get('Field455') == 'Yes':
                    submission.need_custom_software = True
                else:
                    submission.need_custom_software = False
                laptop_description += 'Need Custom Software: %s\n' % (submission.need_custom_software)
                submission.other_laptop_requirements = self.request.POST.get('Field456')
                laptop_description += 'Other Requirements:%s\n' % (submission.other_laptop_requirements)
            else:
                submission.create_laptop_request = False

            # Page 5 - Electrical Request
            if self.request.POST.get('Field338') == 'Yes':
                quartermaster_description = description
                submission.create_power_request = True
                quartermaster_description += 'Power Request:\n'
                if self.request.POST.get('Field341'):
                    submission.num_power_strips = int(self.request.POST.get('Field341'))
                    quartermaster_description += 'Number of Power Strips: %d\n' % (submission.num_power_strips)
                if self.request.POST.get('Field342'):
                    submission.num_25ft_cords = int(self.request.POST.get('Field342'))
                    quartermaster_description += 'Number of 25ft Cords: %d\n' % (submission.num_25ft_cords)
                if self.request.POST.get('Field343'):
                    submission.num_50ft_cords = int(self.request.POST.get('Field343'))
                    quartermaster_description += 'Number of 50ft Cords: %d\n' % (submission.num_50ft_cords)
                submission.other_power_requirements = self.request.POST.get('Field344')
                quartermaster_description += 'Other Power Requirements:%s\n' % (submission.other_power_requirements)
            else:
                quartermaster_description = description
                submission.create_power_request = False

            # Page 6 - Misc. Requests
            # Phone Request
            if self.request.POST.get('Field462') == 'Yes':
                submission.create_phone_request = True
                if self.request.POST.get('Field463'):
                    submission.num_phones = int(self.request.POST.get('Field463'))
                    network_description += 'Number of IP Phones: %d\n' % (submission.num_phones)
                submission.phone_location = self.request.POST.get('Field464')
                network_description += 'Phone Deployment Location: %s\n' % (submission.phone_location)
                submission.other_phone_requirements = self.request.POST.get('Field575')
                network_description += 'Other Phone Requirements:%s\n' % (submission.other_phone_requirements)
            else:
                submission.create_phone_request = False

            # Radio Request
            if self.request.POST.get('Field346') == 'Yes':
                submission.create_radio_request = True
                quartermaster_description += 'Radio Request:\n'
                if self.request.POST.get('Field347'):
                    submission.num_radios = int(self.request.POST.get('Field347'))
                    quartermaster_description += 'Number of Radios: %d\n' % (submission.num_radios)
                if self.request.POST.get('Field349'):
                    submission.num_headsets = int(self.request.POST.get('Field349'))
                    quartermaster_description += 'Number of Headsets: %d\n' % (submission.num_headsets)
                submission.other_radio_requirements = self.request.POST.get('Field348')
                quartermaster_description += 'Other Radio Requirements: %s\n' % (submission.other_radio_requirements)
            else:
                submission.create_radio_request = False

            # Tape Request
            if self.request.POST.get('Field458') == 'Yes':
                submission.create_tape_request = True
                quartermaster_description += 'Tape Request:\n'
                if self.request.POST.get('Field459'):
                    submission.num_rolls = int(self.request.POST.get('Field459'))
                    quartermaster_description += 'Number of Rolls: %d\n' % (submission.num_rolls)
                submission.other_tape_requirements = self.request.POST.get('Field460')
                quartermaster_description += 'Other Tape Requirements: %s\n' % (submission.other_tape_requirements)
            else:
                submission.create_tape_request = False

            # Other
            submission.other_request = self.request.POST.get('Field466')
            description += 'Other Requests:%s\n' % (submission.other_request)

            # Page 7 - Feedback
            submission.feedback_rating = self.request.POST.get('Field469')
            description += 'Feedback Rating: %s\n' % (submission.feedback_rating)
            submission.feedback_comments = self.request.POST.get('Field467')
            description += 'Feedback Comments: %s\n' % (submission.feedback_comments)

            submission.save()
            
            techops_queue = Queue.objects.get(slug='techops')
            print techops_queue

            master_ticket = Ticket(queue=techops_queue,title='TechOps Requirements submission for %s' % (submission.department), submitter_email=submission.contact_email, description=description)
            master_ticket.save()
           
            sub_tickets = []
            if submission.create_av_request:
               ticket = Ticket(queue=techops_queue,title='A/V Request: %s' % (submission.department), submitter_email=submission.contact_email, description=av_description)
               print ticket
               ticket.save()
               sub_tickets.append(ticket)
            if submission.create_network_request or submission.create_phone_request:
               ticket = Ticket(queue=techops_queue,title='Network Request: %s' % (submission.department), submitter_email=submission.contact_email, description=network_description)
               print ticket
               ticket.save()
               sub_tickets.append(ticket)
            if submission.create_laptop_request:
               ticket = Ticket(queue=techops_queue,title='Laptop Request: %s' % (submission.department), submitter_email=submission.contact_email, description=laptop_description)
               print ticket
               ticket.save()
               sub_tickets.append(ticket)
            if submission.create_power_request or submission.create_radio_request or submission.create_tape_request:
               ticket = Ticket(queue=techops_queue,title='Quartermaster Request: %s' % (submission.department), submitter_email=submission.contact_email, description=quartermaster_description)
               print ticket
               ticket.save()
               sub_tickets.append(ticket)
            
            for ticket in sub_tickets:
                TicketDependency(ticket=master_ticket,depends_on=ticket).save() 

            message = {}
            send_feedback = False
            if submission.feedback_rating:
                send_feedback = True
                message['text'] = '%s %s thinks the TechOps requirement form %s' % (submission.first_name, submission.last_name, submission.feedback_rating)

            if submission.feedback_comments:
                send_feedback = True
                message['text'] = '%s %s thinks the TechOps requirement form %s: ```%s```' % (submission.first_name, submission.last_name, submission.feedback_rating, submission.feedback_comments)

            if send_feedback:
                message['type'] = 'new_feedback'
                message['type_readable'] = 'New Feedback'
                message['channel'] = 'techops-engineroom'
                message_promise = amqp_producer.basic_publish(exchange='magfest.techops.notifications', routing_key='json', body=simplejson.dumps(message))
                amqp_producer.wait(message_promise)
            return api_return(STATUS_OK)
        else:
            return api_return(STATUS_ERROR_PERMISSIONS)

    def api_public_list_queues(self):
        return api_return(STATUS_OK, simplejson.dumps([{"id": "%s" % q.id, "title": "%s" % q.title} for q in Queue.objects.all()]), json=True)


