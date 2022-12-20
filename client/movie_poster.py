from simple_image_download import simple_image_download as simp #pip install simple_image_download
#from google_images_download import google_images_download
import requests
import cv2
import matplotlib
import tkinter
from PIL import ImageTk, Image
import numpy as np
from IPython.display import display
import speech_recognition as sr
#from pynput.keyboard import Key, Controller
import numpy
from utilities import listen_phrase,get_num
from playsound import playsound
from utilities import control_number
import time
import os,glob

class MoviePoster_Visualizer:

    def __init__(self):
        pass
    
    def clean_directory(self):
        for filename in glob.glob('./movie_posters/image*'):
            os.remove(filename) 
    
    def delete_wrong_images(self,num_films,correct_films):
        correct_counter = 0
        corrected_films = []
        for j in range(0,num_films):
            image = cv2.imread('./movie_posters/image_'+str(j)+'.jpg')
            dsize = (200, 300)
            try:
                resized_image = cv2.resize(image, dsize)
                os.rename('./movie_posters/image_'+str(j)+'.jpg','./movie_posters/image_'+str(correct_counter)+'.jpg')
                correct_counter += 1
                corrected_films.append(correct_films[j])
            except:
                os.remove('./movie_posters/image_'+str(j)+'.jpg')
        return correct_counter,corrected_films
                
    
    def get_correct_film_link(self,links):
        for link in links:
            if(link.split('/')[2]=='www.gstatic.com' or link.split('/')[3]=='logos'):
                pass
            else:
                return link
        return "Not found"
    
    def horizontal_stack(self,images):
        dim = len(images)
        horizontal_images = images[0]
        if(dim==1):
            return horizontal_images
        else:
            for i in range(1,dim):
                horizontal_images = numpy.hstack((horizontal_images,images[i]))
            return horizontal_images
    
    def show_movie_posters(self,film_names,r,m):
        self.clean_directory()
        response = simp.simple_image_download
        links = []
        first_correct_films = []
        for film_name in film_names:
            film_urls = response().urls(('movie poster ' + film_name), 10)
            links.append(self.get_correct_film_link(film_urls))
        correctLinks_counter = 0
        film_counter = 0
        for url in links:
            if(url!="Not found"):
                try:
                    #first_correct_films.append(film_names[film_counter])
                    img_data = requests.get(url).content
                    with open('./movie_posters/image_'+str(correctLinks_counter)+'.jpg', 'wb') as handler:
                        handler.write(img_data)
                        first_correct_films.append(film_names[film_counter])
                        correctLinks_counter+=1
                except:
                   pass
            film_counter+=1
        first_num_films = len(first_correct_films)
        num_films,correct_films = self.delete_wrong_images(first_num_films,first_correct_films)
        posters = self.vertical_stack(num_films)
        root = tkinter.Tk()
        img = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(posters, cv2.COLOR_BGR2RGB)))
        panel = tkinter.Label(root, image = img)
        panel.pack(side = "bottom", fill = "both",
                   expand = "yes")
        root.update()
        playsound('./audio/choose_film.mp3')
        numero_scelto = control_number(r,m)-1
        root.destroy()
        return correct_films[numero_scelto]
            
    def vertical_stack(self,num_films):
        images = []
        for j in range(0,num_films):
            image = cv2.imread('./movie_posters/image_'+str(j)+'.jpg')
            dsize = (200, 300)
            resized_image = cv2.resize(image, dsize)
            images.append(resized_image)
        remaining = num_films%4
        if(remaining==0):
            num_rows = num_films//4
        else:
            num_rows = (num_films//4)+1
        if(num_rows==1):
            first_row = self.horizontal_stack(images[0:num_films])
            return first_row
        else:
            missing_images = ((num_rows-1)*4)-num_films
            for j in range(num_films,num_rows*4):
                image = cv2.imread('./movie_posters/black.jpg')
                image = resized_image = cv2.resize(image, dsize)
                images.append(resized_image)
            vertical_images = self.horizontal_stack(images[0:4])
            for i in range(1,num_rows):                
                low_extr = (i*4)
                high_extr = (i*4)+4
                horizontal_images = self.horizontal_stack(images[low_extr:high_extr])
                vertical_images = numpy.vstack((vertical_images,horizontal_images))
            return vertical_images
            

def clean_directory():
    for filename in glob.glob('./movie_posters/image*'):
        os.remove(filename)    

'''
r = sr.Recognizer()
with sr.Microphone(device_index=2) as m:
    r.adjust_for_ambient_noise(m,duration = 5)
films = ['_Queen_of_the_Adventures_of_Priscilla', "_The_Devil's_Advocate", '_Sex', '_Donnie_Brasco_(1997)', '_Alien:_Resurrection_(1997)', '_Pink_Floyd_-_The_Wall_(1982)', '_Dead_Man_Walking_(1995)', '_Amistad_(1997)', '_Cop_Land_(1997)', '_Secrets_&_Lies_(1996)', '_Titanic_(1997)', '_The_River_Wild', '_The_Abyss', "_Bram_Stoker's_Dracula_(1992)", '_True_Lies_(1994)']
#films = ['_Return_of_the_Jedi_(1983)', '_The_Empire_Strikes_Back', '_Star_Wars_(1977)', '_Raiders_of_the_Lost_Ark_(1981)', '_Indiana_Jones_and_the_Last_Crusade_(1989)', '_Dr._Strangelove_or:_How_I_Learned_to_Stop_Worrying_and_Love_the_Bomb_(1963)', '_Sex', '_James_and_the_Giant_Peach_(1996)', '_Natural_Born_Killers_(1994)', '_True_Romance_(1993)', '_Blade_Runner_(1982)', "_The_Devil's_Advocate", "_Ulee's_Gold_(1997)", "_William_Shakespeare's_Romeo_and_Juliet_(1996)", '_The_Wrong_Trousers']
mv = MoviePoster_Visualizer().show_movie_posters(films,r,m)
print(mv)
'''