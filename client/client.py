import socket
import pickle
import features_extract as fe
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import os
from playsound import playsound
import time
import numpy as np
from film_reproduction import reproduce_trailer_film
from movie_poster import MoviePoster_Visualizer
from utilities import control_number,get_num,get_user_info,listen_phrase,recognizeFace,search_microphone_index
from server_connection import serverConnection
import time

class clientHandler:
    def __init__(self):
        self.firstLevel_function()
    
    def firstLevel_function(self):
        server = serverConnection()
        r = sr.Recognizer()
        microphone_index = search_microphone_index()
        if(microphone_index==-1):
            print("No microphone,try again!")
            exit
        #with sr.Microphone(device_index=2) as m:
        with sr.Microphone(device_index=microphone_index) as m:
            r.adjust_for_ambient_noise(m,duration = 5)
        self.sayCommands("first")
        #time.sleep(1)
        text = ''
        while (text != "esci"):
            
            playsound('./audio/command.mp3')
            text = listen_phrase(r,m)
            
            if(text== "login"):
                count = 0
                correct_login = 0
                playsound('./audio/how_many.mp3')
                number = control_number(r,m)
                users = []              
                while (count < number):
                    playsound('./audio/get_ready.mp3')
                    time.sleep(5)
                    playsound('./audio/watch_camera.mp3')
                    startTime = time.time()
                    average_desc = recognizeFace('login',r,m)
                    print("face extraction time execution: ",time.time()-startTime)
                    response = server.sendMessage('login',average_desc,'',[])
                    if (response[1]=="fallimento"):
                        playsound('./audio/unsuccessfull_login.mp3')
                        count = number
                    else:
                        playsound('./audio/successful_login.mp3')
                        splitted_response = response[1].split('_')
                        myobj = gTTS(text=('Ciao '+splitted_response[0]),lang="it",slow=False)
                        myobj.save('./audio/login_name.mp3')
                        playsound('./audio/login_name.mp3')
                        users.append(response[1])
                        count += 1
                        correct_login += 1
                if(correct_login == number):
                    self.secondLevel_function(server,users,r,m)
                    text = "esci"
                else:
                     playsound('./audio/all_logged.mp3')
            
            elif(text == "registrazione"):
                count = 0
                playsound('./audio/how_many.mp3')
                number = control_number(r,m)
                while (count < number):
                    playsound('./audio/get_ready.mp3')
                    time.sleep(5)
                    playsound('./audio/watch_camera.mp3')
                    average_desc = recognizeFace('registration',r,m)
                    name,surname = get_user_info(count,r,m)
                    user_id = name + "_" + surname
                    response = server.sendMessage('registration',average_desc,user_id,[])                    
                    if (response[1]=="fallimento"):
                        playsound('./audio/unsuccessfull_registration.mp3')
                        playsound('./audio/user_again.mp3')
                    else:
                        playsound('./audio/successful_registration.mp3')
                    count = count+1
            
            elif(text == "elimina"):
                playsound('./audio/get_ready.mp3')
                time.sleep(5)
                playsound('./audio/watch_camera.mp3')
                average_desc = recognizeFace('registration',r,m)
                response = server.sendMessage('delete',average_desc,'',[])
                if (response[1]=="fallimento"):
                    playsound('./audio/unsuccessfull_delete.mp3')        
                else:
                    playsound('./audio/successfull_delete.mp3')
            
            elif(text == "esci"):
                playsound('./audio/see_you.mp3')
            
            else:    
                playsound('./audio/unrecognized_command.mp3')
    
    def sayCommands(self,level):
        if(level=="first"):
            playsound('./audio/welcome.mp3')
            playsound('./audio/commands_intro.mp3')
            playsound('./audio/reg.mp3')
            playsound('./audio/log.mp3')
            playsound('./audio/delete.mp3')
            playsound('./audio/exit.mp3')
        else:
            playsound('./audio/services.mp3')
            playsound('./audio/film.mp3')
            playsound('./audio/music.mp3')
            playsound('./audio/news.mp3')
            playsound('./audio/exit.mp3')
        time.sleep(1)
            
    
    def secondLevel_function(self,server,users,r,m):
        self.sayCommands("second")
        text = ''
        while (text != "esci"):
            playsound('./audio/second_command.mp3')
            text = listen_phrase(r,m)
            if(text == "film"):
                response = server.sendMessage('film_request','','',users)
                films = response[1].split('/')
                print(films)
                film_scelto = MoviePoster_Visualizer().show_movie_posters(films,r,m)
                reproduce_trailer_film(film_scelto)
                '''
                rf = Reproduce_Film()
                rf.reproduce_trailer_film(film_scelto)
                '''
            elif(text == "musica"):
                playsound('./audio/no_service.mp3')
            elif(text == "news"):
                playsound('./audio/no_service.mp3')
            elif(text == "esci"):
                playsound('./audio/see_you.mp3')
            else:    
                playsound('./audio/unrecognized_command.mp3')



        
if __name__ == '__main__':
    #client_program()
    clientHandler()
