from socket import *

class Client:
    def __init__(self):
        self.host = '192.168.2.210'
        self.port = 9999
        self.addr = (self.host,self.port)
        self.bufsize = 1024
        self.tcpClient = socket(AF_INET, SOCK_STREAM)
        self.tcpClient.connect(self.addr)

    def send(self,msg):
        try:
            self.tcpClient.send(msg.encode(encoding="utf-8"))
            data = self.tcpClient.recv(self.bufsize).decode(encoding="utf-8")
            return data
        except Exception as e:
            print(e)
            return "ERROR SEND!"

    def close(self):
        self.tcpClient.close()





