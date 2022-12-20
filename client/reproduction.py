from mongoConn import Connection_DB
from film_sugg import Film_Suggestor
from film_reproduction import Reproduce_Film
from movie_poster import MoviePoster_Visualizer
import random

def prova():
    
    cd = Connection_DB()
    users = ['matteo_dessi','fabiana_ritorti']
    interest = [cd.get_random_best_common_interests(users,'film_interest')]
    fs = Film_Suggestor()
    films = fs.provide_suggestions(interest)
    numero = MoviePoster_Visualizer().show_movie_posters(films)
    #rf = Reproduce_Film()
    #rf.reproduce_trailer_film(films[numero])
    
    

if __name__ == '__main__':

    prova()