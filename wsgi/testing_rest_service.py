from wsgi_server import *
from rest_client import *
import concurrent.futures
import time


with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.submit(roulette_server, 4)
    print("server is started")
    time.sleep(2)
    print("requests")
    json_get()
    json_get()
    json_get("/european/")
    json_get("/european/")
    
