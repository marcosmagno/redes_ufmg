import socket   
import sys  
import struct
import binascii
class Client(object):

    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', 2222))
        self.host = host
        self.port = port

    def sen(self, msg):
        try:
            header = struct.pack('!H', 1)        
            msg =  header + msg_r
            self.s.sendto(msg, (self.host, self.port))
            self.s.settimeout(4)
        except socket.timeout:          
            print("closing socket")
            

    def send(self, msg):
        self.sen(msg)
        Restramitir = True 
        try:
            while (Restramitir):
                data, d = self.s.recvfrom(1024)
                if data:
                    msg_type = struct.unpack('!H',data[:2])[0]
                    value = data[2:]
                    print '\nResposta de %s na porta %d:'% d
                    print value
                else:
                    print '\nErro na mensagem'
                    print msg_type
                    print value
                    print "recv", msg_type,d
            Restramitir = False                    
                    
        except socket.timeout:       
            Restramitir = False
            self.sen(msg)
            print("Nada a Receber")





if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Numero incorreto de argumentos.\nUso: <IP:port>')
    else:
        ip,port = sys.argv[1].split(':')
        client = Client(ip, int(port))
        msg_r = raw_input('Enter message to send : ')

        client.send(msg_r)


