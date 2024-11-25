# carritodecompras/apps.py

from django.apps import AppConfig

class CarritodecomprasConfig(AppConfig):
    name = 'carritodecompras'

    def ready(self):
        import carritodecompras.signals
