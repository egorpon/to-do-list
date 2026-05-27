"""
WSGI config for to_do_list project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from config.env import env

os.environ.setdefault('DJANGO_SETTINGS_MODULE', env.str('DJANGO_SETTINGS_MODULE', default='config.django.local'))

application = get_wsgi_application()
