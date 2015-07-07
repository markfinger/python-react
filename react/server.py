import json
import hashlib
import requests
from .conf import settings
from .exceptions import RenderServerError


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
            raise RenderServerError('Could not connect to render server at {}'.format(self.url))

        if res.status_code != 200:
            raise RenderServerError(
                'Unexpected response from render server at {} - {}: {}'.format(self.url, res.status_code, res.text)
            )

        return res.json()


server = RenderServer(settings.RENDER_URL)
