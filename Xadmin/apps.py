from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class XadminConfig(AppConfig):
    name = 'Xadmin'

    def ready(self):
        autodiscover_modules('Xadmin')
