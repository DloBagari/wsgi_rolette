from hashlib import sha256
import os
import sys

class Authentication:
    """works with Bytes not Unicode Strings"""
    __iterations =1000
    __slots__ = ("__salt", "__hash", "__username")
    def __init__(self, username, password):
        if not(isinstance(username, bytes) or isinstance(password, bytes)):
            print("class works with bytes only not uncodes")
            print("Usage: Authenication(b'username', b'password')")
            sys.exit()
        #generate unique 24 random bytes
        self.__salt = os.urandom(24)
        self.__username = username
        self.__hash = self._iter_hash(self.__iterations, self.__salt,
                                      username, password)

    @staticmethod
    def _iter_hash(iterations, salt, username, password):
        seed = salt + b":" + username + b":" + password
        #creating repeated hash 
        for i in range(iterations):
            seed = sha256(seed).digest()
        return seed
    
    """since each object is going to have unque salt , even if
       two object has same username and same passowrd they will not be
       equal ever"""
    def __eq__(self, other):
        return self.__username == other.getUsername() and \
               self.__hash == other.getHash()

    #{0:x} represent the field(which is byte) as hex
    def __repr__(self):
        salt_x = "".join("{0:x}".format(b) for b in self.__salt)
        hash_x = "".join("{0:x}".format(b) for b in self.__hash)
        return "{username} {iterations:d}:{salt}:{hash}".format(\
            username = self.__username, iterations = self.__iterations,
            salt = self.__salt, hash = self.__hash)
    
    #required to make object immutable
    def __hash__(self):
        return hash(self.__hash)

    def match(self, password):
        test = self._iter_hash(self.__iterations, self.__salt,
                               self.__username, password)
        
        # constant time is best
        """application must take some time to check the data
           and return some result, we let application takes some
           time to make sure that if the attackers try to guess
           the result it will let them to spend much more time.
           """
        return self.__hash == test 

    def getUsername(self):
        return self.__username
    

    def getHash(self):
        return self.__hash
    
    
