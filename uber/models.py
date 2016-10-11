from __future__ import unicode_literals
import os
from rpctools.jsonrpc import ServerProxy
from datetime import datetime

from django.db import models
from django.conf import settings

def get_ssl_directory(instance, filename):
    directory = os.path.join(settings.BASE_DIR, 'media', 'api_keys', instance.slug)
    return os.path.join(directory, filename)


class Event(models.Model):
    slug = models.SlugField(max_length=24, verbose_name='Short Name', blank=False)
    api_url = models.URLField(verbose_name='Uber API Url', blank=False)
    ssl_client_key = models.FileField(upload_to=get_ssl_directory, blank=True)
    ssl_client_cert = models.FileField(upload_to=get_ssl_directory, blank=True)
    api_version = models.CharField(max_length=8, verbose_name='API Version', blank=True)

    name = models.CharField(max_length=64, verbose_name='Name', blank=True)
    org_name = models.CharField(max_length=64, blank=True, verbose_name='Organization Name')
    year = models.CharField(max_length=4, blank=True)
    epoch = models.DateTimeField(blank=True,null=True, default=datetime(1970,01,01,0,0))

    venue = models.CharField(max_length=128, verbose_name='Venue Name', blank=True)
    venue_address = models.CharField(max_length=128, verbose_name='Venue Address', blank=True)

    at_the_con = models.BooleanField(blank=True)
    post_con = models.BooleanField(blank=True)

    def pull_api_values(self, *args, **kwargs):
        uber = ServerProxy(
            uri=self.api_url,
            cert_file=self.ssl_client_cert.name,
            key_file=self.ssl_client_key.name
        )

        instance_config = uber.config.info()

        self.api_version = instance_config['API_VERSION']
        self.name = instance_config['EVENT_NAME']
        self.org_name = instance_config['ORGANIZATION_NAME']
        self.year = instance_config['YEAR']
        self.epoch = instance_config['EPOCH']

        self.venue = instance_config['EVENT_VENUE']
        self.venue_address = instance_config['EVENT_VENUE_ADDRESS']

        self.at_the_con = instance_config['AT_THE_CON']
        self.post_con = instance_config['POST_CON']
        self.save()

