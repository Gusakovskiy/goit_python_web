# How To
# https://docs.djangoproject.com/en/3.2/topics/http/middleware/
from typing import Callable


class MyMiddleware:

    def __init__(self, get_response: Callable):
        self._get_response = get_response

    def __call__(self, request):
        print('GOT request', request)
        # init global vars
        response = self._get_response(request)
        return response
