import numpy as np
import pandas as pd
import chardet
import random

class Film_Suggestor:

    def __init__(self):        
        self.columns_name=['user_id','item_id','rating','timestamp']
        self.ratings=pd.read_csv("./ml-100k/u.data",sep="\t",names=self.columns_name)        
        with open('./ml-100k/u.item', 'rb') as f:
            enc = chardet.detect(f.read())
        self.movies=pd.read_csv("./ml-100k/u.item",encoding = enc['encoding'],sep="\|",header= None)
        self.movies=self.movies[[0,1,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]]
        self.movies.columns=['item_id','title','unknown','Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western'] 
        self.df=pd.merge(self.ratings,self.movies,on="item_id")
        self.df.groupby("title").mean()['rating'].sort_values(ascending=False)
        self.df.groupby("title").count()["rating"].sort_values(ascending=False)
        self.ratings=pd.DataFrame(self.df.groupby("title").mean()['rating'])
        self.ratings['number of ratings']=pd.DataFrame(self.df.groupby("title").count()["rating"])
        self.ratings.sort_values(by='rating', ascending=False)
        self.moviematrix=self.df.pivot_table(index="user_id",columns="title",values='rating')
        
    def cold_start(self,interests):
      candidates = self.movies
      for interest in interests:
        candidates = candidates.loc[candidates[interest]>0]
      candidates=pd.merge(self.ratings,candidates,on="title")
      candidates.sort_values(by='rating', ascending=False)
      candidates = candidates[candidates['rating']>3.5]
      return candidates[candidates['number of ratings']>50].sort_values('rating',ascending=False)
      
    def predict_movies(self,movie_name):
        movie_user_ratings=self.moviematrix[movie_name]
        similar_to_movie=self.moviematrix.corrwith(movie_user_ratings)
        corr_movie=pd.DataFrame(similar_to_movie,columns=['correlation'])
        corr_movie.dropna(inplace=True)
        corr_movie=pd.merge(self.ratings,corr_movie,on="title")
        #corr_movie=corr_movie.join(self.ratings['number of ratings'])
        corr_movie=corr_movie[corr_movie['rating']>3.0]
        predictions=corr_movie[corr_movie['number of ratings']>50].sort_values('correlation',ascending=False)
        return predictions.head(5)

    def provide_suggestions(self,interests):
      candidates = self.cold_start(interests)
      #titles = candidates.head(3)['title']
      titles = random.sample(list(candidates['title']),3)
      suggestion = []
      for title_name in titles:
        suggestion_of_film = list(self.predict_movies(title_name).index.values)
        for single_suggestion in suggestion_of_film:
          suggestion.append(self.reconstruct_title(single_suggestion))
      mylist = list(dict.fromkeys(suggestion))
      return mylist  
    
    def reconstruct_title(self,name_film):
        splitted_name_film = name_film.split(',')
        reconstructed_title = ""
        if(len(splitted_name_film)==1):
            splitted_pieces = splitted_name_film[0].split()
            for piece in splitted_pieces:
                reconstructed_title = reconstructed_title + '_' + piece
        else:
            first_pieces = splitted_name_film[0].split()
            second_pieces = splitted_name_film[1].split()
            for i in range(0,len(second_pieces)-1):
                reconstructed_title = reconstructed_title + '_' + second_pieces[i]
            for piece in first_pieces:
                reconstructed_title = reconstructed_title + '_' + piece
        return reconstructed_title
    
   
'''
consigliati = Film_Suggestor().provide_suggestions(["Action"])
for consigliato in consigliati:
    print(consigliato)
'''