import requests
import json
import sqlite3
from bs4 import BeautifulSoup
# import csv
from random import randint

h={'Accept-language': 'en-US'}
# f = open('movies.csv', 'w', encoding='utf-8', newline='\n')
# file = csv.writer(f)
# file.writerow(['Film Description', 'Genre', 'IMDB'])
img = []
ind = 1

while ind <6:
    url = "https://srulad.com/movies/page/"+str(ind)
    r = requests.get(url, headers=h)
    soup = BeautifulSoup(r.text, 'html.parser')
    sub_soup= soup.find('div', class_='row')


    all_movies = sub_soup.find_all('div', class_='card movie-item')
    all = []
    for movie in all_movies:
        description = movie.h2.text
        imdb = movie.span.text
        image = movie.img.attrs['data-src']
        nwimage = f'https://srulad.com/{image}'

        genre=movie.find('div', class_='card-genre').text
        # file.writerow([description, genre, imdb])
        default = None
        all.append((description,genre,default,imdb,nwimage))
        img.append(nwimage)


    ind+=1
# print(img)

conn = sqlite3.connect('films.sqlite3')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS films
                      (description VARCHAR(100),
                      genre VARCHAR(30),
                      com VARCHAR(30),
                      imdb VARCHAR(30),
                      img VARCHAR(100))
                      """)

cursor.executemany('INSERT INTO films (description,genre,com,imdb,img) VALUES(?,?,?,?,?)',all)
conn.commit()
# f.close()