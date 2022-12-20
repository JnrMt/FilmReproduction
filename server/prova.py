from csvConn import csvConn
from mongoConn import Connection_DB
from client_utilities import recognizeFace
import speech_recognition as sr
import numpy as np



r = sr.Recognizer()
with sr.Microphone() as m:
    r.adjust_for_ambient_noise(m,duration = 5)
average_desc = recognizeFace('registration',r,m)

'''
#registrazione
csvConn().regUser('matteo_dessi',average_desc)
Connection_DB().insertUser('matteo_dessi')
'''

'''
#login
username = csvConn().searchUser(average_desc,'')
print(username)


total_descs = []
total_ids = []

try:
    total_ids = np.load('./registration/informations/names.npy').tolist()
    total_descs = np.load('./registration/informations/descs.npy').tolist()
except:
    pass
print(total_ids)
print(len(total_descs))
'''

'''
#delete
username = csvConn().searchUser(average_desc,'')
if (username == "none"):
    print("utente non trovato")
else:
    csvConn().deleteUser(username)
    Connection_DB().deleteUser(username)

try:
    total_ids = np.load('./registration/informations/names.npy').tolist()
    total_descs = np.load('./registration/informations/descs.npy').tolist()
except:
    pass
print(total_ids)
print(len(total_descs))

username = csvConn().searchUser(average_desc,'')
print(username)
'''