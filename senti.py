from sqlalchemy.sql.elements import Null
import config.config
from flask import Flask, request , jsonify, render_template
import tools.database as db
from tools.tools import plotsongs, plotartist
import os
print(" - - - Iniziando API")
app = Flask(__name__, template_folder='templates')
print(" - - - Carga Flask", app)

#////////////////////////////////    GET    /////////////////////////////////////////////////////

@app.route("/", methods=["POST", "GET"])

def index():
    """[summary] Returns "Index" as root
    """
    return "Index"

@app.route("/songfromid/<id>")
def getsongfromid(id):
    """[summary] Returns a complete song data from its id
    """
    data=db.get_song_from_id(id)
    return jsonify(data)

@app.route("/allsongs/")
def allsongs():
    """[summary] Returns all the songs in the data base
    """
    data=db.all_songs()
    return jsonify(data)

@app.route("/allartists/")
def allartists():
    """ Returns all the artists in de data base
    """
    data=db.all_artists()
    return jsonify(data)

@app.route("/songsfromartistid/<id>")
def getsongsfromartistid(id):
    """[summary] Returns all the songs for a given artist by its id
    """
    print("- - - Entra en getsongsfromartistid")
    print(id)
    data=db.get_songs_from_artist_id(id)
    return jsonify(data)

@app.route("/songsfromartistname/<name>")
def getsongsfromartistname(name):
    """[summary] Returns all the songs for a given artist by its name

    """
    print("- - - Entra en getsongsfromartistname")
    data=db.get_songs_from_artist_name(name)
    return jsonify(data)

@app.route("/lowestcomsong/<n>")
def lowestcomsong(n=None):
    """ Returns n lowets sentimental rate in the database
    """
    print("- - - Entra en topnegative/<n>")
    data=db.lowest_com_song(n)
    return jsonify(data)

@app.route("/highestcomsong/<n>")
def highestcomsong(n=None):
    """[summary] Returns n hishest sentimental rate in the database

    Args:
        n ([type], optional): [description]. Defaults to None.

    Returns:
        [json]: [if none or error it will be empty]
    """
    data=db.highest_com_song(n)
    return jsonify(data)

@app.route("/countsongsbyartist/")
def countsongsbyartist():
    """[summary] Count songs from every artist in the database

    Returns:
        [json]: [dict with info]
    """
    data=db.count_songs_by_artist()
    return jsonify(data)
#////////////////////////////////    PLOT    /////////////////////////////////////////////////////
@app.route("/plothighestcomsong/<n>", methods=["POST"])
def plothighestcomsong(n=None):
    """[summary] This funcitions returns html containnig the figurer with the ranking information of the n highst rate in ythe database

    Args:
        n ([int], optional): [number of songs]. Defaults to None.

    Returns:
        [html]: [png embbed]
    """
    data=db.highest_com_song(n)
    os.system('rm static/*.png')
    new_graph_name=plotsongs(data)
    h=render_template('output.html',graph=new_graph_name)
    return h
@app.route("/plotartisthist/<name>", methods=["POST"])
def plotartisthist(name):
    """[This funcion returns html containning png image with sentimental hist for an artist]

    Args:
        name ([str]): [name of the artist]

    Returns:
        [html]: [html with png embbed]
    """
    data=db.get_songs_from_artist_name(name)
    os.system('rm static/*.png')
    new_graph_name=plotartist(data)
    h=render_template('output.html', graph=new_graph_name)
    return h

#////////////////////////////////    POST    /////////////////////////////////////////////////////
@app.route("/drop", methods=["POST"])
def eliminar():
    """Drops all the schems and tables in db

    Returns:
        str: Load done or error
    """
    print("- - - Entra en drop")
    return db.eliminar()

@app.route("/create", methods=["POST"])
def create():
    """Creates all the schemas and tables in our db

    Returns:
        str: created or error
    """
    print("- - - Entra en create")
    return db.crea()

@app.route("/load", methods=["POST"])
def load():
    """This function loads in the database all the info from ./data/songs.csv (containg title lyric and artist columns)

    Returns:
        str: loaded or error
    """
    print("- - - Entra en load")
    return db.load()

@app.route("/delete", methods=["POST"])
def delete():
    """Delets all the info in the database

    Returns:
        str: deleted or error
    """
    return db.delete()

@app.route("/newsong", methods=["POST"])
def newsong():
    """Includes a new song in the data base
        ?title=***&?artist=***?lyric=***
    Returns:
        json: info from the song in the database/error string
    """
    try:
        titulo=request.args.get("title",None)
        artista = request.args.get("artist", None)
        letra = request.args.get("lyric", None)
        data = db.intro_cancion(titulo, artista, letra)
        return jsonify(data)
    except:
        return "error"

@app.route("/newartist/<artist>", methods=["POST"])
def nuevoartista(artist):
    """Add new artist by its name

    Args:
        artist (str): name of the artis

    Returns:
        json: info of the artist in the db/error string
    """
    try:
        data = db.intro_artist(artist)
        return jsonify(data)
    except:
        return "error"

@app.route("/deletesongbyid/<id>", methods=["POST"])
def deletesongbyid(id):
    """delets a song in the db by its id

    Args:
        id (int): id in the database

    Returns:
        json: jason with the info in the database. if not in void. if error "error"
    """
    try:
        return db.delete_song_by_id(id)
    except:
        return "error"

@app.route("/deleteartisandsongbyidartist/<id>", methods=["POST"])
def deleteartisandsongbyidartist(id):
    """Delete an artist and all songs releated .

    Args:
        id (int): id of the artist in the database

    Returns:
        string: "Songs and artist deleted" or "error"
    """
    try:
        return db.delete_artist_and_song_by_idartist(id)
    except:
        return "error"

@app.route("/conectsongartist/", methods=["POST"])
def conectsongartist():
    """Connect a song to another artist. Delets previos connection

    Returns:
        json: info from the song
    """
    try:
        id_song=request.args.get("id_song",None)
        id_artist = request.args.get("id_artist", None)
        return db.conect_song_artist(id_song,id_artist)
    except:
        return "error"

app.run("localhost", 5000, debug=True)