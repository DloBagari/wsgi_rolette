import random
from collections.abc import Callable
import json
import wsgiref.util
import sys

class BaseWheel(Callable):
    def __init__(self):
        self.bins = [ {str(n):(35,1),
                       self.redblack(n): (1,1),
                       self.hilo(n): (1,1),
                       self.eventodd(n): (1,1),
                       } for n in range(1, 37)]
        self.rng = random.Random()

    def __call__(self, environ, start_response):
        winner = self.spin()
        status = "200 OK"
        headers = [("Content-Type", "application/json; charset=utf-8")]
        start_response(status, headers)
        return [json.dumps(winner).encode("UTF-8")]
    
    
    @staticmethod
    def redblack(n):
        return "Red" if n in (1, 3, 5, 7, 9, 12, 14, 16, 18,
                              19, 21, 23, 25, 27, 30, 32, 34, 36) else "Black"

    @staticmethod
    def hilo(n):
        return "Hi" if n >= 19 else "Lo"

    @staticmethod
    def eventodd(n):
        return "event" if n % 2 == 0 else "Odd"

    def spin(self):
        return self.rng.choice(self.bins)

    def __str__(self):
        return str(self.bins)


#bin for zero and double zero
class Zero:
    def __init__(self):
        super().__init__()
        self.bins += [{"0": (35,1)}]

class ZeroDouble:
    def __init__(self):
        super().__init__()
        self.bins += [{"00": (35,1)}]

#subclasses that define the kind of wheels

#american
class American(Zero, ZeroDouble,BaseWheel ):
    pass

#european
class European(Zero,BaseWheel):
    pass


class Wheel(Callable):
    def __init__(self):
        self.am = American()
        self.eu =European()
    def __call__(self, environ, start_response):
        request = wsgiref.util.shift_path_info(environ)
        print("Wheel", request, file = sys.stderr)
        if request.lower().startswith("eu"):
            response = self.eu(environ, start_response)
        else:
            response = self.am(environ, start_response)
        return response
        
