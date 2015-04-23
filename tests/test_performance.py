import os
import time
import unittest
from .utils import clean_bundle_root
from react.render import render_component

path_to_component = os.path.abspath(os.path.join(os.path.dirname(__file__), 'components', 'PerfTestComponent.jsx'))


def median(l):
    half = int(len(l) / 2)
    l.sort()
    if len(l) % 2 == 0:
        return (l[half-1] + l[half]) / 2.0
    else:
        return l[half]


class TestReactPerformance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        clean_bundle_root()

    @classmethod
    def tearDownClass(cls):
        clean_bundle_root()

    def test_performance(self):
        print('\n' + ('-' * 80))
        print('python-react performance test')
        print('-' * 80)

        render_component_times = []
        render_watched_component_times = []
        rendered_components = []

        iteration_count = 25

        for i in range(iteration_count):
            start = time.time()
            rendered_components.append(
                render_component(
                    path_to_component,
                    props={'name': 'world'},
                    translate=True,
                    to_static_markup=True
                )
            )
            end = time.time()
            render_component_times.append(end - start)

        for i in range(iteration_count):
            start = time.time()
            rendered_components.append(
                render_component(
                    path_to_component,
                    props={'name': 'world'},
                    translate=True,
                    watch_source=True,
                    to_static_markup=True
                )
            )
            end = time.time()
            render_watched_component_times.append(end - start)

        for component in rendered_components:
            self.assertEqual(str(component), '<span>Hello world</span>')

        print('Total time taken to render a component {iteration_count} times: {value}'.format(
            iteration_count=iteration_count,
            value=sum(render_component_times)
        ))
        print('Times: {}'.format(render_component_times))
        print('Max: {}'.format(max(render_component_times)))
        print('Min: {}'.format(min(render_component_times)))
        print('Mean: {}'.format(sum(render_component_times) / len(render_component_times)))
        print('Median: {}'.format(median(render_component_times)))

        print('\nTotal time taken to render a watched component {iteration_count} times: {value}'.format(
            iteration_count=iteration_count,
            value=sum(render_watched_component_times)
        ))
        print('Times: {}'.format(render_watched_component_times))
        print('Max: {}'.format(max(render_watched_component_times)))
        print('Min: {}'.format(min(render_watched_component_times)))
        print('Mean: {}'.format(sum(render_watched_component_times) / len(render_watched_component_times)))
        print('Median: {}'.format(median(render_watched_component_times)))