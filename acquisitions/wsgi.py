"""
WSGI config for acquisitions project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
from cfenv import AppEnv

env = AppEnv()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acquisitions.settings")

# Initialize New Relic monitoring if on Cloud Foundry
if env.name:
    new_relic = env.get_service('acquisitions-new-relic')
    new_relic_license = new_relic.credentials['NEW_RELIC_LICENSE_KEY']
    new_relic_app_name = os.environ.get('NEW_RELIC_APP_NAME')
    if new_relic_license and new_relic_app_name:
        new_relic_settings = newrelic.agent.global_settings()
        new_relic_settings.license_key = new_relic_license
        new_relic_settings.app_name = new_relic_app_name
        newrelic.agent.initialize()

# Whitenoise import must come after settings are loaded
from whitenoise.django import DjangoWhiteNoise

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
