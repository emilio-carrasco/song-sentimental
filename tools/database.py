
from collections import namedtuple
from sqlalchemy.engine import result
from config.config import engine
import pandas as pd
from tools.nlp import sentimental
from tools.tools import cleantext

def crea():
    engine.execute("CREATE DATABASE IF NOT EXISTS lyrics;")   
    engine.execute((f"""USE lyrics;"""))   
    engine.execute((f"""
        CREATE TABLE IF NOT EXISTS lyrics.artist (
        id_artist INT NOT NULL AUTO_INCREMENT,
        name VARCHAR(4100) NULL DEFAULT NULL,
        PRIMARY KEY (id_artist))
        ENGINE = InnoDB
        AUTO_INCREMENT = 148
        DEFAULT CHARACTER SET = utf8mb4
        COLLATE = utf8mb4_0900_ai_ci;
        """))   
    
    engine.execute((f"""
        CREATE TABLE IF NOT EXISTS lyrics.song (
        id_song INT NOT NULL AUTO_INCREMENT,
        title VARCHAR(200) NOT NULL,
        lyric VARCHAR(2000) NOT NULL,
        neg FLOAT NULL DEFAULT NULL,
        neu FLOAT NULL DEFAULT NULL,
        pos FLOAT NULL DEFAULT NULL,
        com FLOAT NULL DEFAULT NULL,
        song_id_artist INT NOT NULL,
        PRIMARY KEY (id_song),
        INDEX fk_song_artist_idx (song_id_artist ASC) VISIBLE,
        CONSTRAINT fk_song_artist
            FOREIGN KEY (song_id_artist)
            REFERENCES lyrics.artist (id_artist))
        ENGINE = InnoDB
        AUTO_INCREMENT = 26542
        DEFAULT CHARACTER SET = utf8mb4
        COLLATE = utf8mb4_0900_ai_ci;
        """))     
    return ("Tables created")
def eliminar():
    engine.execute(f"""
    DROP DATABASE lyrics;""")
    return "DROPPED DB"    
def id_titulo(titulo):
    query = (f"""
    INSERT INTO song(title,lyric,senti,song_id_artist)
    SELECT "{titulo}", "{letra[0:1999]}" as let,{senti} as sen , "{id_resultado}" as iden
    FROM dual
    WHERE NOT EXISTS (SELECT title FROM song WHERE title = "{titulo}")LIMIT 1   
    """)
    engine.execute(query)
    return 
def intro_cancion(titulo, artista, letra):
    # 2do hacer una función que adecue los strings
    artista = cleantext(artista)
    titulo = cleantext(titulo)
    letra = cleantext(letra)
    #print(artista," - - ",titulo)
    if artista!='' and titulo!='' and letra!='':
        senti = sentimental(letra)
        query = (f"""
        INSERT INTO artist (name)
        SELECT * FROM (SELECT "{artista}") AS tmp
        WHERE NOT EXISTS (SELECT name FROM artist WHERE name = "{artista}");    
        """)
        result=engine.execute(query)

        query = (f"""
        SELECT id_artist
        FROM artist WHERE name = "{artista}";    
        """)
        result=engine.execute(query)
        id_resultado =result.fetchone()[0]

        query = (f"""
        INSERT INTO song(title,lyric,neg,pos,neu,com,song_id_artist)
        SELECT "{titulo}", "{letra[0:1999]}" as let,{senti.get('neg')} as neg ,{senti.get('pos')} as pos ,{senti.get('neu')} as neu ,{senti.get('compound')} as com, "{id_resultado}" as iden
        FROM dual
        WHERE NOT EXISTS (SELECT title FROM song WHERE title = "{titulo}")LIMIT 1   
        """)
        resultado=engine.execute(query)
        id_cancion=resultado.lastrowid
        return get_song_from_id(id_cancion)
    else:
        return  
def load():
    path = './data/'
    f = 'songs.csv'
    df = pd.read_csv(path+f)
    df=df[['title','artist','lyric']]
    df.dropna(how='any',inplace=True)
    for r in df.iterrows():
        #print(r[1].title," - del panda - ", r[1].artist)
        intro_cancion(r[1].title, r[1].artist, r[1].lyric)
    return "Loaded"
def delete():
    query = (f"""
    SET SQL_SAFE_UPDATES = 0;
    """)
    engine.execute(query)
    query = (f"""
    DELETE FROM song;
    """)
    engine.execute(query)
    query = (f"""
    DELETE FROM artist;
    """)
    engine.execute(query)
    return "Deleted"
def get_song_from_id(id):
    query = (f"""
    SELECT s.*, a.name
    FROM song as s
    JOIN artist as a ON s.song_id_artist = a.id_artist 
    WHERE s.id_song = "{id}"; """)
    df=pd.read_sql_query(query,con=engine)
    return df.to_dict(orient='records')
def get_songs_from_artist_id(id):
    query = (f"""
    SELECT *
    FROM song WHERE song_id_artist = "{id}";    
    """)
    df=pd.read_sql_query(query,con=engine)
    return df.to_dict(orient='records')
def intro_artist(artista):
    artista = cleantext(artista)
    if artista!='':
        query = (f"""
        INSERT INTO artist (name)
        SELECT * FROM (SELECT "{artista}") AS tmp
        WHERE NOT EXISTS (SELECT name FROM artist WHERE name = "{artista}");    
        """)
        result=engine.execute(query)
        id=result.lastrowid
        return get_artist_from_id(id)
    else:
        return
def get_artist_from_name(name):

    query = (f"""
    SELECT * FROM lyrics.artist WHERE name = "{name}";    
    """)
    result=engine.execute(query)
    df=pd.read_sql_query(query,con=engine)
    return df.to_dict(orient='records')
def get_artist_from_id(id):
    query = (f"""
    SELECT * FROM lyrics.artist WHERE id_artist = "{id}";    
    """)
    result=engine.execute(query)
    df=pd.read_sql_query(query,con=engine)
    return df.to_dict(orient='records')
def get_songs_from_artist_name(name):
    query = (f"""
    SELECT s.*, a.name
    FROM song as s
    JOIN artist as a ON s.song_id_artist = a.id_artist 
    WHERE a.name = "{name}";    
    """)
    
    df=pd.read_sql_query(query,con=engine)
    return df.to_dict(orient='records')
def delete_song_by_id(id):
    query=(f""" DELETE FROM song 
    WHERE id_song = {id}""")
    result=engine.execute(query)
    return "Song deleted"
def delete_artist_and_song_by_idartist(id):
    query=(f""" DELETE FROM song 
    WHERE song_id_artist = {id}""")
    result=engine.execute(query)
    query=(f""" DELETE FROM artist 
    WHERE id_artist = {id}""")
    result=engine.execute(query)
    return "Songs and artist deleted"
def all_songs():
    query=(f"""
    SELECT s.*, a.name
    FROM song as s
    JOIN artist as a ON s.song_id_artist = a.id_artist;    
    """)
    df=pd.read_sql_query(query,con=engine)
    return df.to_dict(orient='records')
def count_songs_by_artist():
    query=(f"""
    SELECT 
    song_id_artist,
    COUNT(song_id_artist)
    FROM lyrics.song
    GROUP BY song_id_artist;
    """)
    df=pd.read_sql_query(query,con=engine)
    return df.to_dict(orient='records')
def all_artists():
    query=(f"""SELECT * FROM lyrics.artist;""")
    df=pd.read_sql_query(query,con=engine)
    return df.to_dict(orient='records')
def lowest_com_song(n=None):    
    if n:
        query=(f"""SELECT * FROM lyrics.song ORDER BY com ASC LIMIT {n};""")
    else:
        return

    df=pd.read_sql_query(query,con=engine)
    return df.to_dict(orient='records')
def highest_com_song(n=None):    
    try:
        query=(f"""SELECT * FROM lyrics.song ORDER BY com DESC LIMIT {n};""")
        df=pd.read_sql_query(query,con=engine)
        return df.to_dict(orient='records')
    except:
       return "Error"
    
def conect_song_artist(id_song,id_artist):
    try:
        query=(f"""
        UPDATE song
        SET song.song_id_artist={id_artist}
        WHERE song.id_song={id_song};""")
        df=pd.read_sql_query(query,con=engine)
        return df.to_dict(orient='records')
    except:
       return "Error"
