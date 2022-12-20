import pymongo
from datetime import datetime
from getpass import getpass
from pprint import pprint
import numpy as np
import os
import re
import random

class Connection_DB:

    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db=self.myclient['IA']
            
    def close(self):
        if self.myclient != "":
            self.myclient.close()

    def deleteUser(self,username):
        self.db.Data.delete_one({"name":username})
    
    def get_all_interest(self):
        films_interests = ['Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western']
        musics_interests = ['Alternative','Anime','Blues','Children','Classical','Country','Dance','Disney','Eletronic','Enka','Hip-Hop','Rap','Indie','Industrial','Instrumental','K-Pop','Jazz','Latin','Metal','Opera','New Age','Reggae','Rock','Vocal']
        all_interests = ['Advocacy','Comics','Crime','Enterprise','Environmental','Fashion','Innovation','Investigative','Gossip','Medical','Online','Science','Service','Social','Sport','Trade','Video Game','Sci-Fi','Thriller','War','Western']
        return random.sample(films_interests,3),random.sample(musics_interests,3),random.sample(all_interests,3)

    def get_random_best_common_interests(self,names,interest_type):
        string = self.interest_string(interest_type)
        interests = list(self.db.Data.aggregate([{"$match":{"name":{"$in":names}}},{"$unwind":string},{"$group":{"_id":string,"count":{"$sum":1}}},{"$sort":{"count":-1}}]))
        #if not interests or interests[0]["count"]==1:
        if not interests:
            return self.get_random_interest(interest_type)
        else:
            max_pop = interests[0]["count"]
            selected_interests = []
            for interest in interests:
                if(interest["count"]<max_pop):
                    break
                else:
                    selected_interests.append(interest["_id"])
                return random.choice(selected_interests)
            
    def get_random_interest(self,interest_type):
        all_interests = []
        if(interest_type=="film_interest"):
            all_interests = ['Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western']
        elif(interest_type=="music_interest"):
            all_interests = ['Alternative','Anime','Blues','Children','Classical','Country','Dance','Disney','Eletronic','Enka','Hip-Hop','Rap','Indie','Industrial','Instrumental','K-Pop','Jazz','Latin','Metal','Opera','New Age','Reggae','Rock','Vocal']
        
        else:
            all_interests = ['Advocacy','Comics','Crime','Enterprise','Environmental','Fashion','Innovation','Investigative','Gossip','Medical','Online','Science','Service','Social','Sport','Trade','Video Game','Sci-Fi','Thriller','War','Western']
        return random.choice(all_interests)       
    
    def insertUser(self,name):
        music_interest = []
        film_interest = []
        news_interest = []
        film_interest,music_interest,news_interest = self.get_all_interest()
        user = {}
        user["name"]=name
        user["film_interest"] = film_interest
        user["music_interest"] = music_interest
        user["news_interest"] = news_interest
        self.db.Data.insert_one(user)
    
    def interest_string(self,interest_type):
        if(interest_type=="film_interest"):
            return "$film_interest"
        elif(interest_type=="music_interest"):
            return "$music_interest"
        else:
            return "$news_interest"
    
    
        
    
    
    
    


