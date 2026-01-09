"""
WSGI config for learningplatform project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Load environment variables from .env.production if it exists
# This file should exist on production servers but not in development
env_file = Path(__file__).resolve().parent.parent / '.env.production'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key, value)

# Default to production settings (override with DJANGO_SETTINGS_MODULE env var)
# For local development, set DJANGO_SETTINGS_MODULE=learningplatform.settings.dev
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learningplatform.settings.production")

application = get_wsgi_application()
