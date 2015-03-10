import os
import time
import unittest
from django_react.render import render_component

path_to_component = os.path.abspath(os.path.join(os.path.dirname(__file__), 'components', 'PerfTestComponent.jsx'))


def median(l):
    half = int(len(l) / 2)
    l.sort()
    if len(l) % 2 == 0:
        return (l[half-1] + l[half]) / 2.0
    else:
        return l[half]


class TestDjangoReactPerformance(unittest.TestCase):
    def test_performance(self):
        print('\n' + ('-' * 80))
        print('django-react performance test')
        print('-' * 80)

        render_component_times = []

        iteration_count = 25

        for i in range(iteration_count):
            start = time.time()
            render_component(path_to_component, '{"name": "world"}')
            end = time.time()
            render_component_times.append(end - start)

        print('Total time taken to render a component {iteration_count} times: {value}'.format(
            iteration_count=iteration_count,
            value=sum(render_component_times)
        ))
        print('Times: {value}'.format(value=render_component_times))
        print('Max: {value}'.format(value=max(render_component_times)))
        print('Min: {value}'.format(value=min(render_component_times)))
        print('Mean: {value}'.format(value=sum(render_component_times) / len(render_component_times)))
        print('Median: {value}'.format(value=median(render_component_times)))