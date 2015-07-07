import json
import hashlib
import requests
from .conf import settings
from .exceptions import RenderServerConnectionError, RenderServerUnexpectedResponse


class RenderServer(object):
    def __init__(self, url):
        self.url = url

    def render(self, options):
        serialized_options = json.dumps(options)
        options_hash = hashlib.sha1(serialized_options.encode('utf-8')).hexdigest()

        try:
            res = requests.post(
                self.url,
                data=serialized_options,
                headers={'content-type': 'application/json'},
                params={'hash': options_hash}
            )
        except requests.ConnectionError:
            raise RenderServerConnectionError('Tried to send build request to {}'.format(self.url))

        if res.status_code != 200:
            raise RenderServerUnexpectedResponse('{}: {}'.format(res.status_code, res.text))

        return res.json()


server = RenderServer(settings.RENDER_URL)
