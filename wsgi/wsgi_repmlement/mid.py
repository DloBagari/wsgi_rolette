from wsgiref.simple_server import make_server
from collections.abc import Callable
from que import *
from wsgiref.simple_server import make_server, WSGIServer
from socketserver import ThreadingMixIn

class ThreadingWSGIServer(ThreadingMixIn, WSGIServer): 
    pass

class MiddleWare(Callable):
    def __init__(self):
        self.__callback = Server()

    def __call__(self):

        httpd = make_server("",8080, self.__callback, ThreadingWSGIServer)
        httpd.serve_forever()

if __name__ == "__main__":
    s = MiddleWare()
    s()
