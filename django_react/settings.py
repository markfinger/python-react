from django.conf import settings

setting_overrides = getattr(settings, 'DJANGO_REACT', {})

SERVICE_URL = setting_overrides.get(
    'SERVICE_URL',
    'http://localhost:63578/render'
)