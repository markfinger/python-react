from django.conf import settings

setting_overrides = getattr(settings, 'DJANGO_REACT', {})

INVALIDATE_CACHE = setting_overrides.get(
    'INVALIDATE_CACHE',
    False
)

NPM_INSTALL_ON_INIT = setting_overrides.get(
    'NPM_INSTALL_ON_INIT',
    True,
)
