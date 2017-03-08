from collections.abc import Callable
import wsgiref.util
import json
from table import *

class WSGI(Callable):
    #this method will be used as abstact method is not implemented
    def __call__(self, environ, start_response):
        raise NotImplementedError

#an exception class to define an error instead of 500 error of wsgiref
class RESTException(Exception):
    pass


class Roulette(WSGI):
    def __init__(self, wheel):
        self.table = Table()
        self.wheel = wheel
        self.rounds = 0

    def __call__(self, environ, start_response):
        app = wsgiref.util.shift_path_info(environ)
        try:
            if app.lower() == "player":
                return self.player_app(environ, start_response)
            elif app.lower() == "bet":
                return self.bet_app(environ, start_response)
            elif app.lower() == "wheel":
                return self.wheel_app(environ, start_response)
            else:
                raise RESTException("404 NOT_FOUNd",
                "Unkown app in {SCRIPT_NAME}/{PATH_INFO}".format_map(environ))
                #format_map() takes dictionary and make it as **kw
        except RESTException as e:
            status = e.args[0]
            headers = [("Content-Type","text/plain; charset=utf-8")]
            start_response(status, headers)
            return [repr(e.args[1]).encode("UTF-*")]

    def player_app(self, environ, start_response):
        if environ["REQUEST_METHOD"] == "GET":
            details = dict( stake = self.table.stake,
                            rounds = self.rounds)
            status = "200 OK"
            headers = [("Content-Type", "application/json; charset=utf-8")]
            start_response(status, headers)
            return [json.dumps(details).encode("UTF-8")]
        else:
            #if method is post or put or delete the exception will be
            #handled in to level __call__()
            raise RESTException("405 METHOD_NOT_ALLOWED",
                "Method '{REQUEST_METHOD}' not allowed".format_map(environ))

    def bet_app(self, environ, start_response):
        """
         this do two things when request method is get:the result is dectionary
         of current bets,
         when POST request is used there most be some data to define bets.
         when any other methods is defined raise exception.
         in the POST request the information of the bets is attached to request
         as stream of bytes,
         we have to preform several steps to read this data,
         the fist step is to find the length of the stream data attached to POST
         by using environ.["CONTENT_LENGTH"] second step is to read there bytes and
         decode them to get string value that eas sent
        """
        if environ["REQUEST_METHOD"] == "GET":
            details = dict(self.table.bets)
        elif environ["REQUEST_METHOD"] == "POST":
            #there will be the way to read the data in the Post method
            size = int(environ["CONTENT_LENGTH"])#length of the body in POST
            #read the body of the Post from file wsgi.input
            #calling "wsgi.input" return opened file of the post databody
            #raw will contain json represantation
            raw = environ["wsgi.input"].read(int(size)).decode("UTF-8")
            try:
                data = json.loads(raw)
                if isinstance(data, dict):
                    data = [data]
                for detail in data:
                    self.table.place_bet(detail["bet"], int(detail["amount"]))
            except Exception as e:
                raise RESTException("403 FORBIDDEN",
                                    "Bet {raw!r}".format(raw=raw))
            details = dict( self.table.bets)
        else:
           raise RESTException("405 METHOD_NOT_ALLOWED",
                "Method '{REQUEST_METHOD}' not allowed".format_map(environ))
        status = "200 OK"
        headers = [("Content-Type", "application/json; charset(utf-8)")]
        start_response(status, headers)
        return [json.dumps(details).encode("UTF-8")]
    
                
    def wheel_app (self, environ, start_response ):
        """method will make sure is type of request is POST and it does not have any data in it
           this to just be sure that socket is properly closed, and no more data coming,
            if there is data all data will read and ignored, this will prevent from
            crashing when the socket is closed with unread data.
        """
        if environ["REQUEST_METHOD"] == "POST":
            size = environ["CONTENT_LENGTH"]
            if size != "":
                raw = environ["wsgi.input"].read(int(size)).decode("UTF-8")
                raise RESTException("403 FORBIDDEN",
                                    "DATA {raw!r} not Allowed".format(raw=raw))
            spin = self.wheel.spin()
            payout = self.table.resolve(spin)
            self.rounds += 1
            details = dict(spin=spin, payout=payout, stake = self.table.stake,
                            rounds=self.rounds)
            
            status = "200 OK"
            headers = [("Content-Type","application/json; charset=utf-8")]
            start_response(status, headers)
            return [json.dumps(details).encode("UTF-8")]
        else:
           raise RESTException("405 METHOD_NOT_ALLOWED",
                "Method '{REQUEST_METHOD}' not allowed".format_map(environ)) 
