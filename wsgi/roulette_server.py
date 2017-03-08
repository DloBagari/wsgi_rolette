#!/usr/bin/python3
from wheel_roulrette import *
from wsgiref.simple_server import make_server
from wsgiref.validate import validator
import concurrent.futures
import time
from rest_client import *
from collections.abc import Callable
from table import *
from roulette_app import *

class Roulette_server(Callable):
    def __init__(self):
        self.wheel = American()
        self.roulette = Roulette(self.wheel)

    def __call__(self, count=None):
        #validate the interface used by the  wsgi appication
        #it validate with assert statement
        #it provide easy to read error messages in wsgi application
        debug = validator(self.roulette)
        httpd = make_server("", 8080, debug)
        if count is None:
            httpd.serve_forever()
        else:
            for c in range(count):
                httpd.handle_request()
if __name__ == "__main__":
    server = Roulette_server()
    server(count=None)
