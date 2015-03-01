from django.conf import settings

setting_overrides = getattr(settings, 'DJANGO_REACT', {})

CACHE_RENDERED_HTML = setting_overrides.get(
    'CACHE_RENDERED_HTML',
    not settings.DEBUG,
)

CACHE_COMPONENT_SOURCE = setting_overrides.get(
    'CACHE_COMPONENT_SOURCE',
    not settings.DEBUG,
)

NPM_INSTALL_ON_INIT = setting_overrides.get(
    'NPM_INSTALL_ON_INIT',
    True,
)
