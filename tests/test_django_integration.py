import json
import datetime
from django.test import TestCase
from django.utils import timezone
from optional_django.env import DJANGO_CONFIGURED
from react.render import render_component
from react import conf
from .settings import Components


class TestDjangoIntegration(TestCase):
    __test__ = DJANGO_CONFIGURED

    def test_can_serialize_datetime_values_in_props(self):
        component = render_component(
            Components.HELLO_WORLD_JSX,
            {
                'name': 'world!',
                'datetime': datetime.datetime(2015, 1, 2, 3, 4, 5, tzinfo=timezone.utc),
                'date': datetime.date(2015, 1, 2),
                'time': datetime.time(3, 4, 5),
            },
        )
        deserialized = json.loads(component.props)
        self.assertEqual(
            deserialized,
            {
                'name': 'world!',
                'datetime': '2015-01-02T03:04:05Z',
                'date': '2015-01-02',
                'time': '03:04:05',
            }
        )

    def test_relative_paths_are_resolved_via_the_static_file_finder(self):
        component = render_component(Components.DJANGO_REL_PATH, to_static_markup=True)
        self.assertEqual(str(component), '<span>You found me.</span>')

    def test_django_settings_are_proxied(self):
        self.assertEqual(conf.settings.RENDER, True)
        with self.settings(REACT={'RENDER': False}):
            self.assertEqual(conf.settings.RENDER, False)

