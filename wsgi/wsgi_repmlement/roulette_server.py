#!/usr/bin/python3

from routette_client import *
import concurrent.futures
import time
from collections.abc import Callable

from wsgiref.simple_server import make_server
from wheel_roulette import *

class Roulette_Server(Callable):
    "making a server to handle a http requests"
    def __init__(self):
        self.__callback = Wheel()

    def __call__(self, count=None):
        #create an object of the make_server
        #host is localhost, port is 8080, callback: which will take request
        #and porcessed and return an response
        httpd = make_server("",8080,self.__callback)
        if count is None:
            httpd.serve_forever()
        else:
            for _ in range(count):
                httpd.handle_request()

if __name__ == "__main__":
    #using multithread to make subprocess to run the server and then continue to
    #process the rest code
    #cconcurrent.futures module is multithread module
    #ProcessPoolExector return an object like newCachedThreadPool() in java
    #and this method is contxt manager which will ensure to close the multithread
    #object like we do in java thread.shutdown()
    server = Roulette_Server()
    server()

        
    
