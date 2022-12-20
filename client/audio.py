import speech_recognition as sr
import os
from subprocess import call
from playsound import playsound
import serial
import RPi.GPIO as GPIO
import pyaudio

def listen_phrase(r,m):
    text = ""
    audio = ""
    firstTime = True
    #print("error later")
    with m as source:
        while(text==""):
            if (firstTime == False):
                playsound('./audio/unknown_response.mp3')
            else:
                firstTime = False
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio,language="it-IT")
            except Exception as e:
                print(e)
    print(text.lower())
    return text.lower()

    
def main():
    myPyAudio = pyaudio.PyAudio()
    #print(myPyAudio.get_device_count())
    print(myPyAudio.get_device_info_by_index(2))
    #print("error 1")
    r = sr.Recognizer()
    #print("error 2")
    with sr.Microphone(device_index=2) as m:
        r.adjust_for_ambient_noise(m,duration = 5)
        #r.energy_threshold = 1000
    #print("error 3")
    listen_phrase(r,m) 
    
    
    
    
if __name__ == "__main__":
	main()