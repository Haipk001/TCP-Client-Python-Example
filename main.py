# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 17:35:57 2022
1. The program template below helps you know how to use the TCP client class 
2. You can listening and sending data from/to TCP server
3. It's aware that this template you can put other program to run simultaneously
with TCP client class
 
@author: Phan Khac Hai homepage: https://khphan.com
"""


import TCPsocket
import time


#Parameters for TCP connection
retryAttempts = 5
remote_IP = "your remote IP"
remote_port = "your port" #it should be a number such as 2000
tcp_time_start = 0
time_start = 0
time_send_bit = 60
tcp_outdata = None
tcp_senddata = None


if __name__ == '__main__':
    
    try:

        # server
        remote_IP = remote_IP
        remote_port = remote_port
        
        # Setting TCP Socket
        tcp = TCPsocket.TCPlient(remote_IP, remote_port, retryAttempts)
        tcp.TCP_Connection(remote_IP, remote_port, retryAttempts)
        
        tcp_time_start = time.time() 
        time_start = time.time() 
         
        while True:
            #Listening commands from server
            tcp.read()
            if tcp.incomingData:
                   
                tcp_outdata = tcp.datasend
                
                print(tcp_outdata)
                tcp.send_to_Server(tcp_outdata, 2)
                tcp.incomingData = False
                
# =============================================================================
#           Put your other program here, for example listing for Endnode device
# =============================================================================
            

            #Remember always keeping your tcp connection staying alive
            if time.time() - tcp_time_start > time_send_bit:
                print("disconnect tcp service")
                tcp.disconnect()
                tcp_time_start = time.time()
            
            if tcp.connectionFailed:
                #Here you can update IP and port every time from external program
                try:
                    remote_IP =  "your new IP"
                    remote_port = "your new port"
      
                except Exception as e:
                    print("Error:")
                    print(e)
                    pass  
                        
                if tcp.attempt < retryAttempts:
                    print("attempt to connect again")
                    tcp.TCP_Connection(remote_IP, remote_port, retryAttempts)
                                                        
                #reset attempt to zero to make tcp reconnecting 
                tcp.attempt = 0 

                
# =============================================================================
#           Put other program here, for example, updating configuration parameters
# =============================================================================
                            
    except Exception as e:
        print("write error into log file")
        print(e)
    finally:
        pass
