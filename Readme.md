![image](https://user-images.githubusercontent.com/80259592/116899204-905b1880-ac37-11eb-8371-19e9bf078dba.png)



Goal 🏁
This is a python project that was sent to us at the Ironhack data analytics bootcamp.

The objective of the project is to you create an API. This API will be able to receive information, store it, or serve it when needed.

Tools ⚙️
The tools to be used are Flask, NLP, functions, string operations, pandas, SQL Alchemy, SQL DB, etc.

LIBRARIES
Pandas
Requests
Os
Time
Nltk
Matplotlib
Seaborn
Collections
SQL Alchemy
Dotenv
Re
Flask
platform
My project


The first thing I did was importing and cleaning a Songs dataset from Kaggle.

https://www.kaggle.com/deepshah16/song-lyrics-dataset

Then runned my appi with different endpoints. All of them running locally with flask.

The endpoints created are:

"http://localhost:5000/" : It gives a first page just "Index" - GET

"http://localhost:5000/create" : Create db schm. and tables on SQL - POST

"http://localhost:5000/load" : Loads all the song in ./data/songs.csv to our DB. Columns must titled: artist,title,lyric for a correct upload - POST

"http://localhost:5000/delete" : delete all data in our DB - POST

"http://localhost:5000/newsong/?title=TITLE&?astist=ARTIST&?lyric=LYRIC" : it will include a new song in db -POST.

"http://localhost:5000/newartist/*artist*" : includes a new artist name in our db. - POST
    
"http://localhost:5000/deletesongbyid/*id**": deletes a song by its id number. POST
    
"http://localhost:5000/deleteartisandsongbyidartis/*id**": delete an artist by its id number. -POST
    
"http://localhost:5000/conectsongartist/?id_song=ID_SONG&?id_artist=ID_ARTIST": reconnect one song to another artist
    
"http://localhost:5000/songfromid/*id**": it returns all the info from a song from its id. -GET
"http://localhost:5000/allsongs/": returns all the songs in the db -GET
    
"http://localhost:5000/allartists/": returns all the artists in the db - GET
    
"http://localhost:5000/songsfromartistid/*id**" : returns all the songs from an artist id. - GET
    
"http://localhost:5000/songsfromartistname/*name*": returns all the songs from an artist name. -GET
    
"http://localhost:5000/lowestcomsong/*n**": it returns the N lowest sentimental rate in the db -GET
    
"http://localhost:5000/highestcomsong/*n**" it returns the N highest sentimental rate in the db -GET

"http://localhost:5000/countsongsbyartist/": iT counts all the songs from each artist in the DB - GET
    
"http://localhost:5000/plothighestcomsong/*n**": it returns the N highest sent rate in the dB figure -POST
    
"http://localhost:5000/plotartisthist/*name**": it returns a hist for an artist by its name figure. - POST

Content of the repository 👀
Src folder with the functions defined and documented
senti.py with the main program
database folder with all the documents required for the API-db managament:
congif folder with configuration
tools folder with the functions
README.md file
Data folder with the csv from Kaggle
templates with the html template necessary for the figures
fig folder to store temporary figures

TO DO
- Deploy Heroku
