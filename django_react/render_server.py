import atexit
import json
import requests
from django_node.settings import PATH_TO_NODE
import subprocess
from requests.exceptions import ConnectionError
from .exceptions import RenderingError, RenderServerStartError
from .settings import (
    RENDER_SERVER_ADDRESS, RENDER_SERVER_PROTOCOL, RENDER_SERVER_PORT, PATH_TO_RENDER_SERVER_SOURCE,
    SHUTDOWN_RENDER_SERVER_ON_EXIT, RENDER_SERVER_DEBUG, RENDER_SERVER_RENDERING_ENDPOINT, RENDER_SERVER_TEST_ENDPOINT,
    RENDER_SERVER_TEST_EXPECTED_OUTPUT, START_RENDER_SERVER_ON_INIT
)


class ReactRenderServer(object):
    """
    A persistent Node server which sits alongside the python process
    and responds over the network to render React components on demand
    """

    address = RENDER_SERVER_ADDRESS
    protocol = RENDER_SERVER_PROTOCOL
    port = RENDER_SERVER_PORT
    path_to_server_source = PATH_TO_RENDER_SERVER_SOURCE
    start_on_init = START_RENDER_SERVER_ON_INIT
    shutdown_on_exit = SHUTDOWN_RENDER_SERVER_ON_EXIT
    test_endpoint = RENDER_SERVER_TEST_ENDPOINT
    test_expected_output = RENDER_SERVER_TEST_EXPECTED_OUTPUT
    render_endpoint = RENDER_SERVER_RENDERING_ENDPOINT
    popen = None
    has_started = False
    has_shutdown = False
    startup_output = None
    server_details_json = None
    server_details = None

    def __init__(self):
        if self.start_on_init:
            self.start()

    def start(self):
        if RENDER_SERVER_DEBUG:
            print('Starting django-react render server')

        if self.shutdown_on_exit:
            atexit.register(self.shutdown)

        # While rendering templates Django will silently ignore some types of exceptions,
        # so we need to intercept them and raise our own class of exception
        try:
            self.popen = subprocess.Popen(
                (PATH_TO_NODE, self.path_to_server_source, '--address', self.address, '--port', self.port),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except (TypeError, AttributeError) as e:
            raise RenderServerStartError(e.__class__.__name__, *e.args)

        startup_output = self.popen.stdout.readline()
        self.startup_output = startup_output.decode()

        if self.startup_output.strip() != 'Started django-react render server':
            self.shutdown()
            self.startup_output += self.popen.stdout.read()
            raise RenderServerStartError(
                'Error starting server: {startup_output}'.format(
                    startup_output=self.startup_output
                )
            )

        server_details_json = self.popen.stdout.readline()
        self.server_details_json = server_details_json.decode()
        self.server_details = json.loads(self.server_details_json)

        # If the server is defining its own address or port, we
        # need to record it
        self.address = self.server_details['address']
        self.port = self.server_details['port']

        # Ensure that we can connect to the server over the network
        if not self.test():
            self.shutdown()
            raise RenderServerStartError(
                'Cannot test server to determine if startup successful. Tried {server_url}'.format(
                    server_url=self.get_server_url()
                )
            )

        self.has_started = True
        self.has_shutdown = False

        if RENDER_SERVER_DEBUG:
            print('django-react render server now listening at {server_url}'.format(
                server_url=self.get_server_url()
            ))

    def get_server_url(self):
        return '{protocol}://{address}:{port}'.format(
            protocol=self.protocol,
            address=self.address,
            port=self.port,
        )

    def get_test_url(self):
        return '{server_url}{test_endpoint}'.format(
            server_url=self.get_server_url(),
            test_endpoint=self.test_endpoint,
        )

    def get_render_url(self):
        return '{server_url}{render_endpoint}'.format(
            server_url=self.get_server_url(),
            render_endpoint=self.render_endpoint,
        )

    def render(self, path_to_source, render_to, path_to_serialized_props=None):
        if not self.has_started:
            self.start()

        if RENDER_SERVER_DEBUG:
            print('Sending render request to the django-react render server at {render_url}'.format(
                render_url=self.get_render_url()
            ))

        render_url = self.get_render_url()

        params = {
            'path-to-source': path_to_source,
            'render-to': render_to,
        }

        if path_to_serialized_props is not None:
            params['path-to-serialized-props'] = path_to_serialized_props

        response = requests.get(render_url, params=params)

        if response.status_code != 200:
            error_message = response.text
            # Convert the error message from HTML to plain text
            error_message = error_message.replace('<br>', '\n')
            error_message = error_message.replace('&nbsp;', ' ')
            # Remove multiple spaces
            error_message = ' '.join(error_message.split())
            raise RenderingError(error_message)

        return response.text

    def shutdown(self):
        if RENDER_SERVER_DEBUG:
            print('Shutting down django-react render server at {server_url}'.format(
                server_url=self.get_server_url()
            ))

        self.has_shutdown = True
        self.has_started = False
        self.popen.terminate()

    def test(self):
        if RENDER_SERVER_DEBUG:
            print('Testing connection to django-react render server at {server_url}'.format(
                server_url=self.get_server_url()
            ))

        try:
            response = requests.get(self.get_test_url())
        except ConnectionError:
            return False

        if response.status_code != 200:
            return False

        return response.text == self.test_expected_output