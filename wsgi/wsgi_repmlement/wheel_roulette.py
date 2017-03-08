import random
from collections.abc import Callable
import json
import wsgiref.util
import sys

class BaseWheel(Callable):
    """receives request ,envirement, start_response objects
       environ is a dictionary of information about the invermenet which made
       the equest
       process and start_response and returned value is the
        body of the response"""

    def __init__(self):
        #sice this class is going to be superclass
        #then all its attribute must not be private must be protected
        #self.__bets will be invisible in subclasses
        self._bets = [{str(bet):(35, 1),
                        self.red_black(bet): (2, 1),
                        self.hi_lo(bet): (2, 1),
                        self.odd_even(bet): (2, 1)
                        } for bet in range(1, 37)]
        self._rand = random.Random()


    def __call__(self, envirn, start_response):
        winner = self.spin()
        #status is 200 and reason is ok
        status = "200 OK"
        headers = [("Content-Type", "application/json; charset=utf-8")]
        #anything is been print as a part of body response before
        #we send the state and the header will raise exception
        start_response(status, headers)
        #anything after sending the status and
        #header will be part of the response
        #returned value is the body of the response object
        return [json.dumps(winner).encode("UTF-8")]

    @staticmethod
    def red_black(bet):
        return "red" if bet in (1, 3, 5, 7, 9, 12, 14, 16, 18,
                19, 21, 23, 25, 27, 30, 32, 34, 36) else "black"

    @staticmethod
    def hi_lo(bet):
        return "hi" if bet >=19 else "lo"

    @staticmethod
    def odd_even(bet):
        return "odd" if bet % 2 !=0 else "even"

    def spin(self):
        return self._rand.choice(self._bets)

    def __str__(self):
        return str(self._bets)


#bets including zero
class Zero:
    def __init__(self):
        super().__init__()
        self._bets += [{"0":(35, 1)}]

class Double_zero:
    def __init__(self):
        super().__init__()
        self._bets += [{"00":(35, 1)}]


#subclass that define the kind of the wheels
class American(Zero, Double_zero, BaseWheel):
    pass

class European(Zero, BaseWheel):
    pass

#class for making choice of which wheel is needed
class Wheel(Callable):
    "choice the request wheel and send response"
    def __init__(self):
        self.__am = American()
        self.__eu = European()

    def __call__(self, environ, start_response):
        #shift a singl name form the path
        #shift_path_info: examine the environ["PATH_INFO"]
        #this will parse one level of the path information and return
        #string value that was found(which is the last part in the path
        #or return None id no path in provided
        request = wsgiref.util.shift_path_info(environ)
        #stderr: is used by interrpeter to define the output
        #as standard error
        #anything is been printed with in WSGI will we counted as part
        #of the response from WSGI where file=sys.stdout which is default for
        #print statment
        #to not make is as part of WSGI esponse we print in stderr
        #we can use this to ask user for something like log in
        #or to show user something even for testing as well
        print("notation:Wheel", request, file=sys.stderr)
        if request.lower().startswith("am"):
            response = self.__am(environ, start_response)
        else:
            response = self.__eu(environ, start_response)
        return response

    
    
