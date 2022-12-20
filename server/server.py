import pickle
from re import search
import socket
import sys
import numpy as np
import time
from csvConn import csvConn
import socketserver
from mongoConn import Connection_DB
from film_sugg import Film_Suggestor
from utilities import get_from_string_to_original,get_users_from_string,get_string_from_array


class MyTCPHandler(socketserver.BaseRequestHandler):

    def get_entire_message(self,connection):
        message = ""
        counter = 0
        while True:       
            message_piece = connection.recv(2000)
            if not message_piece:
                break
            else:
                message_part = message_piece.decode()
                message_part_splitted = message_part.split('_fine_messaggio')
                if(len(message_part_splitted)>1):
                    message += message_part_splitted[0]
                    #print(message_part_splitted[1])
                    break
                else:
                    message += message_part_splitted[0]
        return message.split('new_part_')

    def handle(self):
        # Receiving command from the client
        received_message = self.get_entire_message(self.request)
        print(received_message[1])
        if(received_message[1]=='login'):
            string_array = received_message[2]
            features = get_from_string_to_original(string_array.split('/'))
            username = csvConn().searchUser(features,'')
            print(username)
            if (username == "none"):
                self.request.sendall(('new_part_fallimento_fine_messaggio').encode())
            else:
                self.request.sendall(('new_part_' + username + '_fine_messaggio').encode())
                
        elif(received_message[1]=='registration'):
            username = received_message[2]
            string_array = received_message[3]
            features = get_from_string_to_original(string_array.split('/'))
            username_old = csvConn().searchUser(features,username)
            if (username_old == 'none'):
                csvConn().regUser(username,features)
                Connection_DB().insertUser(username)
                self.request.sendall(('new_part_successo_fine_messaggio').encode())
            else:
                self.request.sendall(('new_part_fallimento_fine_messaggio').encode())    
        
        elif(received_message[1]=='delete'):
            string_array = received_message[2]
            features = get_from_string_to_original(string_array.split('/'))
            username = csvConn().searchUser(features,'')
            print(username)
            if (username == "none"):
                self.request.sendall(('new_part_fallimento_fine_messaggio').encode())
            else:
                csvConn().deleteUser(username)
                Connection_DB().deleteUser(username)
                self.request.sendall(('new_part_successo_fine_messaggio').encode())
        
        else:
            users = get_users_from_string(received_message[2])
            cd = Connection_DB()
            interest = [cd.get_random_best_common_interests(users,'film_interest')]
            cd.close()
            fs = Film_Suggestor()
            films = fs.provide_suggestions(interest)
            string_suggestions = get_string_from_array(films)
            self.request.sendall(('new_part_'+string_suggestions+'_fine_messaggio').encode())

    '''
    def searchUser(self,average_feat,username):
        total_descs = []
        total_ids = []
        try:
            total_ids = np.load('./registration/informations/names.npy')
            total_descs = np.load('./registration/informations/descs.npy')
        except:
            pass
        classifier = on.OneNNClassifier(total_ids, total_descs)
        closest = classifier.predict(average_feat,username)
        if closest == None: #closest == None se non c'è un utente registrato con le mie features oppure se non ci sono descrittori
            return "none"
        else:
            return closest
            
    def reg_user(self,name,features):
        user_names = []
        user_descs = []
        try:
            user_names = np.load('./registration/informations/names.npy').tolist()
            user_descs = np.load('./registration/informations/descs.npy').tolist()
        except:
            pass
        user_names.append(name)
        user_descs.append(features)
        user_names = np.asarray(user_names)
        user_descs = np.asarray(user_descs)
        print(user_descs)
        print(user_names)
        np.save('./registration/informations/names.npy', user_names)
        np.save('./registration/informations/descs.npy', user_descs)
        mongo = Connection_DB()
        mongo.insertUser(name)
    '''


def server_program():
    HOST = socket.gethostbyname(socket.gethostname())
    print("host",HOST)
    PORT = 5000
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
   
if __name__ == '__main__':
    server_program()