
import pickle
import features_extract as fe
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import os
from playsound import playsound
import time
import numpy as np

def control_number(r,m):
    text = listen_phrase(r,m)
    endLoop = True
    number = 0
    while (endLoop):
        number = get_num(text)
        if (number==-1):
            playsound('./audio/unrecognized_number.mp3')
            playsound('./audio/try_again.mp3')
            text = listen_phrase(r,m)
        else:
            endLoop = False
            
    return number

def get_num(text):
    dict={
        'uno': 1,
        'due': 2,
        'tre': 3,
        'quattro': 4,
        'cinque': 5,
        'sei': 6,
        'sette': 7,
        'otto': 8,
        'nove': 9,
        'dieci': 10,
        'undici': 11,
        'dodici': 12,
        'tredici': 13,
        'quattordici': 14,
        'quindici': 15
        }
    try:
        return int(text)
    except:
        return dict.get(text, -1)

def get_user_info(count,r,m):
    user_number = "Utente numero: "+ str(count+1)
    myobj = gTTS(text=user_number,lang="it",slow=False)
    myobj.save('./audio/user_number.mp3')
    playsound('./audio/user_number.mp3')      
    endLoop = True
    name = ""
    count = 0
    while (endLoop):        
        playsound('./audio/name.mp3')
        name = listen_phrase(r,m)
        user_name = "Il nome che ho capito è: "+ name
        myobj = gTTS(text=user_name,lang="it",slow=False)
        myobj.save('./audio/user_name'+str(count%2)+'.mp3')
        playsound('./audio/user_name'+str(count%2)+'.mp3')
        playsound('./audio/control_name.mp3')
        if (listen_phrase(r,m) == "sì"):
                endLoop = False
        else:
            count += 1
    endLoop = True
    surname = ""
    count = 0
    while (endLoop):       
        playsound('./audio/surname.mp3')
        surname = listen_phrase(r,m)
        user_surname = "Il cognome che ho capito è: "+ surname
        myobj = gTTS(text=user_surname,lang="it",slow=False)
        myobj.save('./audio/user_surname'+str(count%2)+'.mp3')
        playsound('./audio/user_surname'+str(count%2)+'.mp3')
        playsound('./audio/control_surname.mp3')
        if (listen_phrase(r,m) == "sì"):
            endLoop = False
        else:
            count += 1
    return name,surname

def listen_phrase(r,m):
    text = ""
    audio = ""
    firstTime = True
    with m as source:
        while(audio==""):
            if (firstTime == False):
                playsound('./audio/unknown_response.mp3')
            else:
                audio = r.listen(source)
                firstTime = False

        try:
            text = r.recognize_google(audio,language="it-IT")
        except Exception as e:
            print(e)
    print(text.lower())
    return text.lower()

def recognizeFace(typeOf,r,m):
    frame,detected_face,average_desc = fe.get_average_features(typeOf)
    endLoop = True
    while(endLoop):
        if (detected_face == []):
            playsound('./audio/unknown_face.mp3')
            playsound('./audio/prepare_face.mp3')
            playsound('./audio/get_ready.mp3')
            time.sleep(5)
            frame,detected_face,average_desc = fe.get_average_features(typeOf)
        else:
            endLoop = False

    return average_desc[0]
