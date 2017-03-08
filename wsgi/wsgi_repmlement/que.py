from collections.abc import Callable
import wsgiref.util
import json
import threading
import time

class Server (Callable):
    def __init__(self):
        self.q = Queue()
        self.message = None

    def __call__(self, environ, start_response):
        lock.acquire()
        try:
            method = environ["REQUEST_METHOD"]
            if method == "GET":
                status = "200 OK"
                headers = [("Content-Type", "application/json; charset=utf-8")]
                start_response(status, headers)
                self.q.pop(self)
                message_available.acquire()
                while self.q.size() == 0:
                    message_available.wait()
                message_available.release()
                    

                return [json.dumps(self.message).encode("UTF-8")]
            elif method == "POST":
                try:
                    length= int(environ.get('CONTENT_LENGTH', '0'))
                except ValueError:
                    length= 0
                if length !=0:
                    message = environ['wsgi.input'].read(length).decode()
                    self.q.append(message)
                    #assert self.q.size() != 0
                    status = "200 OK"
                    headers = [("Content-Type", "application/json; charset=utf-8")]
                    start_response(status, headers)
                    return [json.dumps("item Added").encode("UTF-8")]
                else:
                    status = "403 FORBIDDEN"
                    headers = [("Content-Type", "application/json; charset=utf-8")]
                    start_response(status, headers)
                    return [json.dumps("Error: 403 FORBIDDEN no data Attached").encode("UTF-8")]
                    
                    
            else:
                status = "405 METHOD_NOT_ALLOWED"
                headers = [("Content-Type", "application/json; charset=utf-8")]
                start_response(status, headers)
                return [json.dumps("Error: 405 METHOD_NOT_ALLOWED").encode("UTF-8")]
        finally:
            time.sleep(1)
            lock.release()
            #pass
          
            
            
class Queue():
    def __init__(self):
        self.q = []
        self.message = None
        #self.setMessage = SetMessage(environ, start_response)


    def pop(self, caller):
        
        thread = GetMessage(caller, self.q)
        thread.start()


    def append(self, message):
        
        thread = SetMessage(self.q, message)
        thread.start()
            
        

    def size(self):
        return len(self.q)
        

    
            
class GetMessage(threading.Thread):
    def __init__(self,caller, q):
        super().__init__()
        self.q = q
        self.caller = caller
        
    def run(self):
        message_available.acquire()
        while len(self.q) == 0 :
            print("waiting")
            message_available.wait()
        self.caller.message = self.q.pop()
        message_available.release()


class SetMessage(threading.Thread):
    def __init__(self, q, message):
        super().__init__()
        self.q = q
        self.message = message

    def run(self):
        message_available.acquire()
        self.q.append(self.message)
        message_available.notify_all()
        message_available.release()
        

        
        
lock = threading.Lock()
lock2 = threading.Lock()
lock3 = threading.Lock()
message_available = threading.Condition(lock)

            

