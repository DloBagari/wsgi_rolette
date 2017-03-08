#!/usr/bin/python3
import http.client
import json
import concurrent.futures
import time
import threading
import sys
class MyThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        c = Cleint(self.name)
        c.getitem()
        c.setitem("dd")
        #c.getitem()



    

class Cleint :
    def __init__(self, name):
        self.name = name
        self.rest = http.client.HTTPConnection("localhost", 8080)

    def setitem(self, item):

        self.rest.request("POST","/", body = item)
        response = self.rest.getresponse()
        row = response.read().decode("UTF-8")
        if response.status == 200:
            print(json.loads(row))
        else:
            print(json.loads(row), file=sys.stderr)


    def getitem(self):

        self.rest.request("GET","/get")
        response = self.rest.getresponse()
        row = response.read().decode("UTF-8")
        if response.status == 200:
            print(str(json.loads(row))+ " thread " + self.name)




   
        
lock = threading.Lock()         
if __name__ == "__main__":
    t1 = MyThread("1")
    t2 = MyThread("2")
    t3 = MyThread("3")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.submit(t1.start())
        #executor.submit(t2.start())
        #executor.submit(t3.start())
            


   
