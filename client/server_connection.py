import socket
import pickle
import pyttsx3
import os
import numpy as np

class serverConnection:
    
    def __init__(self):
        pass
        
    def create_message(self,type,features,name,users):
        data = ''
        if(type=='login'):
            data = 'new_part_login'
            string_array = self.get_string_from_array(features)
            data += 'new_part_'
            data += string_array
            data += '_fine_messaggio'
        
        elif(type=='registration'):
            data = 'new_part_registration'
            data += 'new_part_'
            data += name
            data += 'new_part_'
            string_array = self.get_string_from_array(features)
            data += string_array
            data += '_fine_messaggio'
        
        elif(type=='delete'):
            data = 'new_part_delete'
            string_array = self.get_string_from_array(features)
            data += 'new_part_'
            data += string_array
            data += '_fine_messaggio'
        
        elif(type=='film_request'):
            data = 'new_part_film_request'
            data += 'new_part_'
            data += self.get_user_string_from_array(['matteo_dessi','fabiana_ritorti'])
            data += '_fine_messaggio'
        
        else:
            pass
        return data
    
    def get_entire_message(self,connection):
        message = ""
        counter = 0
        while True:
            message_piece = connection.recv(2000)
            if not message_piece:
                print('non ho letto nulla')
                break
            else:
                message_part = message_piece.decode()
                message_part_splitted = message_part.split('_fine_messaggio')
                if(len(message_part_splitted)>1):
                    message += message_part_splitted[0]
                    break
                else:
                    message += message_part_splitted[0]
                counter+=1
        return message.split('new_part_')
    
    def get_from_string_to_original(self,string_array):
        array = []
        for string in string_array:
            array.append(float(string))
        return np.asarray(array)

    def get_string_from_array(self,average_desc):
        return "/".join(str(x) for x in average_desc)

    def get_user_string_from_array(self,users):
        return "/".join(x for x in users)


    def sendMessage(self,type,features,name,users):
        data = self.create_message(type,features,name,users)
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect(('192.168.1.107', 5000))
        tcp_socket.sendall(data.encode())
        response = self.get_entire_message(tcp_socket)
        tcp_socket.close()
        return response
        