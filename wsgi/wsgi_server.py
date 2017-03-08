#!/usr/bin/python3
from wheel_roulrette import *
from wsgiref.simple_server import make_server
import concurrent.futures
import time
from rest_client import *
from collections.abc import Callable

class Server(Callable):
    def __init__(self):
        self.wheel = Wheel()
    
    def __call__(self,count=None):
       with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.submit(self._roulette_server, count)
            print("server is starting")
            time.sleep(2)
            #json_get() 

    def _roulette_server(self,count=None):
        httpd = make_server("", 8080, self.wheel)
        if count is None:
            httpd.serve_forever()
        else:
            for c in range(count):
                httpd.handle_request()



"""exector : ProcessPoolExecutor is multiprocess it need to run
in multiprocess supporter like terminale python idle does not sport
multiporcessing for this reason ve have to test this script in terminal"""



if __name__ == "__main__":
    server = Server()
    server(10)
    
    




