"""creating a REST client
the http.client module has four step process
1- establish a http connection viea HTTPConnection("localhost", port)
2- to send a request to the server  with command and path
3- to get the response
4-to read and process the response
"""
import re
import http.client
import json
from collections.abc import Callable

class Roulette_client(Callable):

    def __init__(self):
        super().__init__()

    def __call__(self, path="/"):
        #in host parameter we have to specify the host name
        #we can not but "" for localhost
        #the name of the service must be defined
        rest = http.client.HTTPConnection("localhost",8080)
        #make request with method get 
        rest.request("GET", path)
        response = rest.getresponse()
        #display respnse info
        #print(response.status, response.reason)
        #print(response.getheaders())
        #get the charset
        content_header = response.getheader("Content-Type")
        pattren = re.compile(r".*charset=(.*$)")
        match = pattren.match(content_header)
        charset = match.group(1) if match else "UTF-8"

        row = response.read().decode(charset)
        if response.status == "200":
            print(json.loads(row))
        else:
            print(row)

if __name__ == "__main__":
    client = Roulette_client()
    client("/am")
        

