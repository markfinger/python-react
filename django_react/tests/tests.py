import unittest
from django_react.models import ReactComponent
from django_react.exceptions import RenderingError, PropSerialisationError


class TestDjangoReact(unittest.TestCase):
    def test_can_inherit_from_react_component(self):
        class Component(ReactComponent):
            pass

    def test_can_instantiate_a_react_component(self):
        class Component(ReactComponent):
            pass
        Component()

    def test_can_render_a_react_component(self):
        class Component(ReactComponent):
            pass
        Component().render()

    def test_can_bundle_a_react_component(self):
        class Component(ReactComponent):
            pass
        Component().render()