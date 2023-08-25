# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 09:25:39 2022
this class has referred to here: https://stackoverflow.com/questions/17963485/python-socket-connection-class
@author: Phan Khac Hai homepage: https://khphan.com
"""

import socket
import select
import time
import sys

class TCPlient():

    def __init__(self, host, port, retryAttempts = 10 ):

        self.time_connect = 0
        self.host = host
        self.port = port
        self.retryAttempts = retryAttempts
        self.attempt = 0
        self.tcp_socket = None
        self.connectionFailed = True
        self.datasend = None
        self.incomingData = False
        
    def TCP_Connection(self,host, port, retryAttempts):
        self.attempt = 0
        self.retryAttempts = retryAttempts
        print("tcp is connecting.......")
        while self.attempt < self.retryAttempts:
            self.host = host
            self.port = port
            self.connect()
            if self.connectionFailed:   
                self.attempt = self.attempt + 1
                print('attempt to reconnecting ' + str(self.attempt))
                time.sleep(5)
                self.time_connect = time.time()
                self.connect()
            else:
                print('TCP connected ' + str(self.attempt))
                self.send_to_Server('Send data to server to check OK \r\n OK', 2)
                self.retryAttempts = 0
                break
               
    def connect(self):
        try:
            self.tcp_socket = socket.socket()
            self.tcp_socket.settimeout(10)
        except socket.error as e:
            print(e)
            self.tcp_socket = None
            pass
            
        try:
            self.tcp_socket.connect((self.host, self.port))
            print("TCP opened")
            self.connectionFailed = False
        except socket.error as e:
            print(e)
            self.tcp_socket.close()
            self.tcp_socket = None
            self.connectionFailed = True
            pass
    

    def disconnect(self):
        if self.tcp_socket:
            try:
                self.tcp_socket.close()
                self.tcp_socket = None
                self.connectionFailed = True
            except socket.error as e:
                print(e)
                pass
        else:
            self.connectionFailed = True
        

    def send_to_Server(self, buf_data, is_byte):
        while self.connectionFailed == False:
            try:

                if is_byte == 1:
                    data_byte = buf_data
                    self.tcp_socket.sendall(data_byte)
                    print("sent byte data to server succeeded!")
                    break
                else:
                    data_enc = (buf_data).encode()
                    self.tcp_socket.sendall(data_enc)    
                    print("sent string data to server succeeded!")
                    break    

            except socket.error:   
                pass
    
    
    def read(self, timeout = 0.1):
        while self.connectionFailed == False:
            rlist, wlist, xlist = select.select([self.tcp_socket], [],
                                                        [],timeout)
            if not (rlist or wlist or xlist):
                break
            else:
                if len(rlist) != 0:
                    try:
                        data = self.tcp_socket.recv(1024)
                    except socket.error as e:
                        print(e)
                        self.tcp_socket.close()
                        self.tcp_socket = None
                        self.connectionFailed = True
                        sys.exit(1)
                        break
                    else:
                        if len(data) == 0:
                            print('orderly shutdown on server end')
                            self.tcp_socket.close()
                            self.tcp_socket = None
                            self.connectionFailed = True
                            self.attempt = 0
                            break
                        else:
                            # got a message do something :)  
                            dec_data = data.decode()   
                            self.datasend = dec_data
                            self.incomingData = True
                            break
                else:
                    break
    
    
    def reConnection(self, host, port):    
        while True:
            print("reconnection.......")
            self.TCP_Connection(host, port)
            if self.connectionFailed == False:
                break
            
