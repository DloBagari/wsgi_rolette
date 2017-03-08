import http.client
import json
import concurrent.futures
import time


def json_get(path="/"):
    rest = http.client.HTTPConnection("localhost", 8080)
    rest.request("GET", path)
    response = rest.getresponse()
    #print(response.status,response.reason)
    #print(response.getheaders())
    row = response.read().decode("UTF-8")
    if response.status == 200:
        document = json.loads(row)
        return document
    return None


if __name__ == "__main__":
    print(json_get())
