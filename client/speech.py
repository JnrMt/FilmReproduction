import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import os
from playsound import playsound

def SpeakText(command):
	engine = pyttsx3.init()
	engine.say(command)
	engine.runAndWait()
    
def main():

    
    welcome_text = "Per favore rispondere con sì oppure no"
    myobj = gTTS(text=welcome_text,lang="it",slow=False)
    myobj.save('./audio/yes_or_no.mp3')




    
    
    
    # welcome_text = "I comandi disponibili sono:"
    # myobj = gTTS(text=welcome_text,lang="it",slow=False)
    # myobj.save("commands_intro.mp3")
    # welcome_text = "Registrazione"
    # myobj = gTTS(text=welcome_text,lang="it",slow=False)
    # myobj.save("reg.mp3")
    # welcome_text = "Login"
    # myobj = gTTS(text=welcome_text,lang="it",slow=False)
    # myobj.save("log.mp3")
    # '''
    # '''
    # print("Start recognition \n")
    # r = sr.Recognizer()
    # text = ""
    # with sr.Microphone() as source:
    #     r.adjust_for_ambient_noise(source)
    #     print("Sono in ascolto...parla pure!")
    #     audio = r.listen(source)
    #     print("ok! sto elaborando il messaggio")
    #     try:
    #         text = r.recognize_google(audio,language="it-IT")
    #         print("Ho capito: \n",text)
    #     except Exception as e:
    #         print(e)
    # if(text=="saluta"):
    #     hello_text = "Ciao Fabiana"
    #     myobj = gTTS(text=hello_text,lang="it",slow=False)
    #     myobj.save("hello.mp3")
    #     playsound("hello.mp3")
    
    
if __name__ == "__main__":
	main()