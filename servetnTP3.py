import socket
import sys
import struct
import binascii
MSG_TYPE_SIZE = 2

class Servent(object):
    """docstring for Servent"""
    def __init__(self, recv_port, file ):   
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = recv_port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # Create Datagram Socket (UDP)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', self.port)) #Accept Connections on port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.dicionario_mensagem = set()
        self.seq_number = 0
        print "dicionario msg", self.dicionario_mensagem
        self.ttl = 3
        self.count = 0

    def set_neighbors(self, neighbors): 
        self.neighbors_dict = neighbors
        

    def get_neighbors(self):
        return self.neighbors_dict

    def read_file(self):
        print "files"
        
    def msg_query(self):
        self.ttl = 3


    def decode_CLIRESQ(self, chave, address):
        nei = self.get_neighbors()
        msg_type_query = struct.pack('!H', 2)
        ipcliente = address[0]
        ip_inet = socket.inet_aton(ipcliente)  
        portoClient = address[1]        
        ip = address
        port = 2222
        
        chave = chave      
        
        #if (ipcliente, portoClient, self.seq_number, chave) not in self.dicionario_mensagem:
        self.dicionario_mensagem.add((ipcliente, portoClient, self.seq_number, chave))
        #print "dicionario msg", self.dicionario_mensagem
            # verifica no arquivo
            #self.__check_for_chave((ip, port), chave)
        self.seq_number += 1
        print self.seq_number
        send_query = str(msg_type_query) + str(self.ttl)  + str(self.seq_number) + str(port) + str(ip_inet) + str(chave) 
        for x in nei:            
            split_x = str(x).split(":")
            dest_source = (''+split_x[0]+'' , int(split_x[1]))                     
            self.s.sendto(send_query, (dest_source))


    def decode_QUERY(self, msg):
        nei = self.get_neighbors()
        msg_type_query = struct.pack('!H', 2)

        self.count +=1 
        print "count: ", self.count
        print "+++++++\n\n" , msg
        

        type_msg =  msg[:1] 
        print "TYPE MSG: ", type_msg    
        ttl = msg[1:2]
        print "TTL", ttl
        n_sequencia = msg[2:3]
        print "N SEQUANDI", n_sequencia
        
        portoClient = msg[2:6]      
        print "PORT CLIENTE", portoClient
        ipcliente = socket.inet_ntoa(msg[6:10])
        print "IP CLIENTE", ipcliente
        chave = msg[10:]
        print "CHAVE", chave
        ip_inet = socket.inet_aton(ipcliente)
     
        #msg_t = msg[:1]
        #print msg_t
        #dd = socket.inet_ntoa(msg[2:6])
        #print dd
       # 2310,0,0,31
        print "dicionario: ", self.dicionario_mensagem
        print ipcliente, portoClient, n_sequencia, 

        if (ipcliente, portoClient, n_sequencia, chave) not in self.dicionario_mensagem:
            self.dicionario_mensagem.add((ipcliente, portoClient, n_sequencia, chave))
            print "dicionario msg", self.dicionario_mensagem

        elif (ipcliente, portoClient, n_sequencia, chave) in self.dicionario_mensagem:
            print "Ja tem"

        

        int(ttl)  
        print ttl

        if self.ttl > 0 :
            # verifica no arquivo
            #self.__check_for_chave((ip, port), chave)
        #self.seq_number += 1
            send_query = str(msg_type_query) + str(self.ttl)  + str(self.seq_number) + str(portoClient) + str(ip_inet) + str(chave) 
            for x in nei:            
                split_x = str(x).split(":")
                dest_source = (''+split_x[0]+'' , int(split_x[1]))                     
                self.s.sendto(send_query, (dest_source))



        m = "OK"
        dest_source = (''+ipcliente+'' , int(portoClient)) 
        self.server.sendto(m, (dest_source))

        
    def decode_msg(self, data, address_recv):
        msg_type = struct.unpack('!H',data[:2])[0]
        chave = data[2:1024]
        #print "\nreceived message:", chave
        #print '\nfrom:',address_recv
        #print '\nmsg type', msg_type

        if (msg_type == 1):            
            self.decode_CLIRESQ(chave,address_recv)
        elif msg_type == 2:
            print "Mensagem 2"
            self.decode_QUERY(chave)

    def recvfrom(self):
        #print "\nWaint...."
        #print "\nConexao :", self.port 
        #print "\nIP: ", self.host  
        while (True):
            message, address = self.server.recvfrom(1024) # Buffer size is 8192. Change as needed. 
                
            if message:                
                #print "addres", address
                self.decode_msg(message, address)              
            


def main():
    
    if len(sys.argv) < 3:
        sys.exit('Numero insufi ciente de argumentos.\n' + 
            'Uso: <localport> <chave-values> <ip1:port1> ... <ipN:portN>')
    else:
        port = int(sys.argv[1])
        input_file = sys.argv[2]
        neighbors = sys.argv[3:]
    
    serv = Servent(port, input_file)
    serv.set_neighbors(neighbors)    
    serv.recvfrom()
    
    

if __name__ == '__main__':
    main()