#!/usr/bin/python3
import http.client
import json
from collections.abc import Callable
from roulette_server import *
import time

#this is gereric client class is not specific for roulette

class Roulette_client(Callable):
    def __init__(self):
        self.rest = http.client.HTTPConnection("localhost", 8080)

    def __call__(self, method="GET", path="/", data=None):
        if data:
            headers = {"Content-Type": "application/json; chatset=utf-8"}
            params = json.dumps(data).encode("UTF-8")
            self.rest.request(method, path, params)
        else:
            self.rest.request(method, path)

        response = self.rest.getresponse()
        raw = response.read().decode("UTF-8")
        if 200 <= response.status < 300:
            document = json.loads(raw)
            return document
        else:
            print(response.status, response.reason)
            print(response.getheaders())
            print(raw)


#testing the client with concurrent.futures
with concurrent.futures.ProcessPoolExecutor() as executor:
    roulette = Roulette_client()
    server = Roulette_server()
    executor.submit(server)
    time.sleep(6)
    print(roulette("GET","/player/"))
    print(roulette("GET","/bet/"))
    print(roulette("POST","/bet/", {"bet": "Black", "amount":2}))
    print(roulette("POST","/wheel/"))
    print(roulette("POST","/heel/"))
    print(roulette("DELETE","/wheel/"))
   
   
    
