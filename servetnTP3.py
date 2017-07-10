import socket
import sys
import struct
import binascii
MSG_TYPE_SIZE = 2
import re

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
        self.input_file = file
        self.values = self.read_file(self.input_file)

    def set_neighbors(self, neighbors):
        self.neighbors_dict = neighbors

    def decoder_RESPONSE(self, value, ipcliente, portoClient):
        ''' Send response to Client '''
        msg_RESPONSE = struct.pack('!H', 3)
        msg_send_ = str(msg_RESPONSE) + str(value)
        self.server.sendto(msg_send_, (''+ipcliente+'' , int(portoClient)))
    
    def verifica_chave(self, key, ipcliente, portoClient):
        ''' check value in dict'''
        print 'Procurando por:', key
        if key in self.values:
            value = self.values[key]
            print 'Valor de',key, 'encontrado:',value
            self.decoder_RESPONSE(value,ipcliente, portoClient)            
        else:
            print 'Valor de',key, 'nao encontrado.'

    def get_neighbors(self):
        return self.neighbors_dict

    def read_file(self, file):
        get = re.compile(r'^\s*([^#\s][^\s]*)\s*([^\s].*[^\s]|[^\s])\s*$')
        try:
            with open(file, 'r') as f:
                return {line.group(1) : line.group(2)
                        for line in map(get.match, f) if line is not None}
        except IOError:
            print >>sys.stderr, 'Error ao tentar ler arquivo.'
        sys.exit(0)
        

    def decode_CLIRESQ(self, chave, address):
        ''' Recev CLIRESQ'''
        nei = self.get_neighbors()
        msg_type_query = struct.pack('!H', 2)
        ipcliente = address[0]
        ip_inet = socket.inet_aton(ipcliente)  
        portoClient = address[1]
        chave = chave      
        ''' Add data in dict of mensagem'''       
        self.dicionario_mensagem.add((ipcliente, portoClient, self.seq_number, chave))
        self.seq_number += 1       
        send_query = str(msg_type_query) + str(self.ttl)  + str(self.seq_number) + str(portoClient) + str(ip_inet) + str(chave) 

        for x in nei:            
            split_x = str(x).split(":")
            dest_source = (''+split_x[0]+'' , int(split_x[1]))                     
            self.s.sendto(send_query, (dest_source))


    def decode_QUERY(self, msg):
        nei = self.get_neighbors()
        msg_type_query = struct.pack('!H', 2)
        ''' Processing of data'''
        self.ttl =  msg[:1]       
        self.seq_number = msg[1:2]       
        type_msg = msg[2:3]       
        portoClient = msg[2:6]  
        ipcliente = socket.inet_ntoa(msg[6:10])       
        chave = msg[10:]

        ip_inet = socket.inet_aton(ipcliente)
        # reliable flooding
        if (ipcliente, portoClient, self.seq_number, chave) not in self.dicionario_mensagem:

            self.dicionario_mensagem.add((ipcliente, portoClient, self.seq_number, chave))          
            send_query = str(msg_type_query) + str(self.ttl)  + str(self.seq_number) + str(portoClient) + str(ip_inet) + str(chave) 
            ttl_local = int(self.ttl) 

            ttl_local = ttl_local - 1
            self.ttl = ttl_local

            '''Verify ttl '''
            if self.ttl > 0 :
                ''' Search in local dict'''
                self.verifica_chave(chave, ipcliente, portoClient)
                ''' Send to neighbors '''
                for x in nei:            
                    split_x = str(x).split(":")
                    dest_source = (''+split_x[0]+'' , int(split_x[1]))                    
                    self.s.sendto(send_query, (dest_source))
            
        elif (ipcliente, portoClient, self.seq_number, chave) in self.dicionario_mensagem:
            print "Pesquisa ja realizada."


        
    def decode_msg(self, data, address_recv):
        # Processing of data
        msg_type = struct.unpack('!H',data[:2])[0]
        chave = data[2:1024]
        if (msg_type == 1):            
            self.decode_CLIRESQ(chave,address_recv)
        elif msg_type == 2:
            self.decode_QUERY(chave)

    def recvfrom(self):
        print "\nWaint...."
        while (True):
            message, address = self.server.recvfrom(1024)                 
            if message:  
                self.decode_msg(message, address)              
            


def main():    
    if len(sys.argv) < 3:
        sys.exit('Numero insuficiente de argumentos.\n' + 
            'Ex: <localport> <chave-values> <ip1:port1> ... <ipN:portN>')
    else:
        port = int(sys.argv[1])
        input_file = sys.argv[2]
        neighbors = sys.argv[3:]
    
    serv = Servent(port, input_file)
    serv.set_neighbors(neighbors)    
    serv.recvfrom()
    
    

if __name__ == '__main__':
    main()