
import logging

import requests

log = logging.getLogger(__name__)

triggers = []


class WebHook(object):

    _registered_hooks = {}

    def __init__(self, hook, url, method, auth, execute, callback=None):
        self.hook = hook
        self.url = url
        self.method = method
        self.authenticate = auth
        self.execute = execute
        self.callback = callback

    @classmethod
    def register_hook(cls, hook, url, method, auth, execute, callback=None):
        if not cls._registered_hooks.get(hook):
            cls._registered_hooks[hook] = []
        web_hook = WebHook(hook, url, method, auth, execute, callback)
        cls._registered_hooks[hook].append(web_hook)

    @classmethod
    def remove_hook(cls, ):
        pass  # TODO

    @classmethod
    def trigger_hook(cls, hook, kwargs):
        for hook in cls._registered_hooks.get(hook, []):
            request = dict(
                url=hook.url,
                method=hook.method
            )
            request = hook.authenticate(request, kwargs)
            if not request:
                continue
            request = hook.execute(request, kwargs)
            if not request:
                continue
            url = request.get("url")
            method = request.get("method")
            log.debug("Making request [%s %s]" % (method, url))
            response = requests.request(**request)
            log.debug("Status code to request [%s %s]: %s" % (method, url, response.status_code))
            if hook.callback:
                hook.callback(response, kwargs)
