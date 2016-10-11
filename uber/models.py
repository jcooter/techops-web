from __future__ import unicode_literals
import os

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.dispatch import receiver
from rpctools.jsonrpc import ServerProxy
from datetime import datetime

from django.db import models
from django.conf import settings

TYPE_CHOICE = (
    ('prod', 'Production'),
    ('dev', 'Development')
)

def get_ssl_directory(instance, filename):
    directory = os.path.join(settings.BASE_DIR, 'media', 'api_keys', instance.slug)
    return os.path.join(directory, filename)


class Event(models.Model):
    slug = models.SlugField(max_length=24, verbose_name='Short Name', blank=False, unique=True, primary_key=True)
    api_url = models.URLField(verbose_name='Uber API Url', blank=False)
    ssl_client_key = models.FileField(upload_to=get_ssl_directory, blank=False)
    ssl_client_cert = models.FileField(upload_to=get_ssl_directory, blank=False)
    api_version = models.CharField(max_length=8, verbose_name='API Version', blank=True)
    type = models.CharField(max_length=8,verbose_name='Instance Type', choices=TYPE_CHOICE, blank=False)

    name = models.CharField(max_length=64, verbose_name='Name', blank=True)
    org_name = models.CharField(max_length=64, blank=True, verbose_name='Organization Name')
    year = models.CharField(max_length=4, blank=True)
    epoch = models.DateTimeField(blank=True,null=True, default=datetime(1970,01,01,0,0))

    venue = models.CharField(max_length=128, verbose_name='Venue Name', blank=True)
    venue_address = models.CharField(max_length=128, verbose_name='Venue Address', blank=True)

    at_the_con = models.BooleanField(blank=True)
    post_con = models.BooleanField(blank=True)

    def __unicode__(self):
        if self.type == 'prod':
            return '{} {}'.format(self.name, self.year)
        else:
            return '{} {} ({})'.format(self.name, self.year, self.slug)

    def save(self, *args, **kwargs):
        if isinstance(self.ssl_client_cert.file, TemporaryUploadedFile):
            cert_file=self.ssl_client_cert.file.temporary_file_path()
            cert_key=self.ssl_client_key.file.temporary_file_path()
        else:
            cert_file=self.ssl_client_cert.name
            cert_key=self.ssl_client_key.name

        uber = ServerProxy(
            uri=self.api_url,
            cert_file=cert_file,
            key_file=cert_key
        )

        instance_config = uber.config.info()

        self.api_version = instance_config['API_VERSION']
        self.name = instance_config['EVENT_NAME']
        self.org_name = instance_config['ORGANIZATION_NAME']
        if instance_config['YEAR']:
            self.year = instance_config['YEAR']
        else:
            self.year = datetime.strptime(instance_config['EPOCH'],'%Y-%m-%d %H:%M:%S.000000').year
        self.epoch = instance_config['EPOCH']

        self.venue = instance_config['EVENT_VENUE']
        self.venue_address = instance_config['EVENT_VENUE_ADDRESS']

        self.at_the_con = instance_config['AT_THE_CON']
        self.post_con = instance_config['POST_CON']
        super(Event, self).save(*args, **kwargs)

@receiver(models.signals.post_delete, sender=Event)
def delete_file(sender, instance, *args, **kwargs):
    if instance.ssl_client_key:
        directory = os.path.dirname(instance.ssl_client_key.path)
        if os.path.isfile(instance.ssl_client_key.path):
            os.remove(instance.ssl_client_key.path)
        if os.path.isfile(instance.ssl_client_cert.path):
            os.remove(instance.ssl_client_cert.path)
        if not os.listdir(directory):
            os.rmdir(directory)

