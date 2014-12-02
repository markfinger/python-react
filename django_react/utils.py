import os
import subprocess
import tempfile
import hashlib
from .settings import ENGINE, RENDERER, BUNDLER, STATIC_ROOT
from .exceptions import ReactComponentRenderToStringException, ReactComponentBundleException


def bundle(component):
    with tempfile.NamedTemporaryFile() as output_file:

        cmd_to_run = (
            ENGINE,
            BUNDLER,
            '--entry', component.get_path_to_source(),
            '--output', output_file.name,
            '--library', component.get_component_variable(),
        )

        # Call the bundler
        popen = subprocess.Popen(cmd_to_run, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        popen.wait()

        # Ensure that an exception is thrown if the bundler throws an error
        stderr = popen.stderr.read()
        if stderr:
            raise ReactComponentBundleException(stderr)

        output_file.seek(0)

        bundled_component = output_file.read()

        md5 = hashlib.md5()
        md5.update(bundled_component)

        # TODO: move this to ReactComponent.get_filename_from_source(bundled_source)
        filename = '{component_name}-{hash}.js'.format(
            component_name=component.get_component_name(),
            hash=md5.hexdigest()
        )

        # TODO Move `bundled` into settings
        path_to_file = os.path.join('bundled', filename)
        abs_path_to_file = os.path.join(STATIC_ROOT, path_to_file)

        dir_to_file = os.path.dirname(abs_path_to_file)
        if not os.path.exists(dir_to_file):
            os.makedirs(dir_to_file)

        with open(abs_path_to_file, 'w+') as bundle_file:
            bundle_file.write(bundled_component)

        return abs_path_to_file


def render(component, to_static_markup=None):
    path_to_component = component.get_path_to_source()

    cmd_to_run = (
        ENGINE,
        RENDERER,
        '--path-to-component', path_to_component,
        '--render-to', 'static' if to_static_markup else 'string',
    )

    # TODO
    # exported_as = component.get_exported_as()
    # if exported_as is not None:
    #     cmd_to_run += ('--exported-as', exported_as)

    serialised_props = component.get_serialised_props()

    with tempfile.NamedTemporaryFile() as props_file, tempfile.NamedTemporaryFile() as output_file:
        props_file.write(serialised_props)
        props_file.flush()
        cmd_to_run += ('--serialised-props', props_file.name)

        # Call the renderer
        popen = subprocess.Popen(cmd_to_run, stdout=output_file, stderr=subprocess.PIPE)
        popen.wait()

        # Ensure that an exception is thrown if the renderer throws an error
        stderr = popen.stderr.read()
        if stderr:
            raise ReactComponentRenderToStringException(stderr)

        output_file.seek(0)

        return output_file.read()