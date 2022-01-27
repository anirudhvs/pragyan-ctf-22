import urllib.parse
from django.http import HttpResponse, HttpRequest
import time, re
from decouple import config
import redis
import json
from django.core import serializers

ADMIN_COOKIE = config('ADMIN_COOKIE')
REGEX = config('REGEX')
REDIS_HOST=config('REDIS_HOST')
REDIS_PORT=config('REDIS_PORT')
REDIS_PASSWORD=config('REDIS_PASSWORD')

# connect to redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        path = urllib.parse.urlparse(request.path).path
        response = self.get_response(request)
        
        if r.get(path):
            response = HttpResponse(r.get(path))
            return response

        if 'secretAuth' in request.COOKIES and request.COOKIES['secretAuth'] == ADMIN_COOKIE:
            r.set(path, response.content)
            r.expire(path, 10)
        return response

