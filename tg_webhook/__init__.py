
import requests


triggers = []


class WebHook(object):

    _registered_hooks = {}

    def __init__(self, hook, method, auth, callback=None):
        self.hook = hook
        self.method = method
        self.auth = auth
        self.callback = callback

    @classmethod
    def register_hook(cls, hook, url, method, auth, callback=None):
        if not cls._registered_hooks.get(hook):
            cls._registered_hooks[hook] = []
        web_hook = WebHook(hook, url, method, auth, callback)
        cls._registered_hooks[hook].append(web_hook)

    @classmethod
    def remove_hook(cls, ):
        pass  # TODO

    @classmethod
    def trigger_hook(cls, hook, kwargs):
        for hook in cls._registered_hooks[hook]:
            request = dict(
                url=hook.url,
                method=hook.method
            )
            hook.authenticate(request, kwargs)
            hook.execute(request, kwargs)
            response = requests.request(**request)
            if hook.callback:
                hook.callback(response, kwargs)
