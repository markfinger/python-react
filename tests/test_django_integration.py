import os
import json
import datetime
from django.utils import timezone
from optional_django.env import DJANGO_CONFIGURED
from react.render import render_component
from .utils import BaseTest
from .settings import COMPONENT_ROOT

HELLO_WORLD_COMPONENT_JSX = os.path.join(COMPONENT_ROOT, 'HelloWorld.jsx')
STATIC_FILE_FINDER_COMPONENT = 'django_test_app/StaticFileFinderComponent.jsx'


class TestDjangoIntegration(BaseTest):
    __test__ = DJANGO_CONFIGURED

    def test_can_serialize_datetime_values_in_props(self):
        component = render_component(
            HELLO_WORLD_COMPONENT_JSX,
            props={
                'name': 'world!',
                'datetime': datetime.datetime(2015, 1, 2, 3, 4, 5, tzinfo=timezone.utc),
                'date': datetime.date(2015, 1, 2),
                'time': datetime.time(3, 4, 5),
            },
            translate=True,
        )
        deserialized = json.loads(component.serialized_props)
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
        component = render_component(STATIC_FILE_FINDER_COMPONENT, to_static_markup=True, translate=True)
        self.assertEqual(str(component), '<span>You found me.</span>')