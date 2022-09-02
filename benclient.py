
import socket
import uos
from ucryptolib import aes
from hashlib import  sha256
from json import loads
ENCODING = "utf-8"
MODE_CBC = 2
GETID = b'/GETID'
class client:
    def __init__(self, host: str, port: int, timeout: int = 10,keyfile="key.sec", buffersize = 4096) -> None:
        self.host = host
        self.port = port
        self.remoteADDR = (host, port)
        self.buffersize = buffersize
        self.s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('0.0.0.0',self.port))
        self.s.settimeout(timeout)
        f = open(keyfile,"rb")
        key = f.read()
        self.key = sha256(key).digest()
        f.close()
    def _send(self,data):
        if type(data) == str:data = bytes(data,ENCODING)
        
        self.s.sendto(GETID, self.remoteADDR)
        encid, _ = self.s.recvfrom(self.buffersize)
        ivid, _ = self.s.recvfrom(self.buffersize)
        id = self._decrypt(encid,ivid,True)
        data = self._encrypt(data)
        js = {'hash':sha256(id+data[0]+data[1]).digest(), 'data':data[0], 'iv':data[1]}
        self.s.sendto(str(js), self.remoteADDR)
        if self.noreturn:
            return {}
        hash, _ = self.s.recvfrom(self.buffersize)
        iv, _ = self.s.recvfrom(self.buffersize)
        data, _ = self.s.recvfrom(self.buffersize)

        if not data: return {}

        
        if self._authentificate(id,data,iv,hash):
            plaintext = self._decrypt(data,iv)
            try:
                return loads(plaintext)["data"]
            except:
                return plaintext
        else:
            raise Exception("Authenfication Error!")

    def _encrypt(self, text):
        if type(text) == str:text = bytes(text,ENCODING)
        iv = uos.urandom(16)
        cipher = aes(self.key, MODE_CBC, iv)
        
        padded = text + " " * (16 - len(text) % 16)
        encrypted = cipher.encrypt(padded)
        return (encrypted,iv)
    def _decrypt(self,encrypted, iv,bytes_value=False):
        if type(encrypted) == str:encrypted = bytes(encrypted,ENCODING)
        decipher = aes(self.key, MODE_CBC, iv)
        decrypted = decipher.decrypt(encrypted).strip()
        if not bytes_value:
            decrypted = decrypted.decode('utf-8') 
        return decrypted
    def _authentificate(self,id,payload,iv,hash):
        mk = id+payload+iv
        hash1 = sha256(mk).digest()
        if hash == hash1:
            return True
        return False
    def send(self,data, noreturn=False):
        self.noreturn = noreturn
        if not type(data) == dict:raise KeyError("Argument must of type dict.")
        data = str(data)
        
        
        try:
            ret = self._send(data)
            return ret
        except OSError as e:
            raise e  