from salt_hash_password import *

class Users(dict):
    "dictionary to store the users"
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self[b""] = Authentication(b"_dummy__", b"doesn't matter")
    def add(self, authentication):
        if authentication.getUsername() == b"":
            raise KeyError("Invalid Authentication")
        self[authentication.getUsername()] = authentication

    def match(self, username, password):
        if username in self and username != b"":# username b"" will never change
            return self[username].match(password)
        
            """why we return false if even the username is not in dict?
            becaause we dont what the other to know if that username is
            exits or no, we dont wnat to give to attacker any informations"""
        else:
            #why we simply doesnt return false
            """we need to use constant time comparsion
            since the match method will take some time to compare
            the data this will create a reply to response
            which is good when we deals with sencetive datas
            to cause the attacker to spend much more time if they try to guess
            the reponse of the comparsion
            to return simply false it takes milliseconds
            to return the result of the constant timming comarsion may take
            seconds"""
            return self[b""].match(b"something which dorent match")
        
            
