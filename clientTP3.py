import socket   #for sockets
import sys  #for exit
import struct
import binascii
 
# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 2222))
except socket.error:
    print 'Failed to create socket'
    sys.exit()
 
host = sys.argv[1]
port = int(sys.argv[2])
 
while(1) :
    msg_r = raw_input('Enter message to send : ')
    header = struct.pack('!H', 1)
    msg =  header + msg_r   
 
    
    try :
        #Set the whole string
        s.sendto(msg, (host, port))

        # receive data from client (data, addr)
        m, d = s.recvfrom(1024)
        
        header = struct.pack('!2s', m)
        print "mensagem",header
        print "recv", d
        #reply = d[0]
        #addr = d[1]
         
        #print 'Server reply : ' + reply
        #m = s.recvfrom(1024)
        #print m
     
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()


s.close()