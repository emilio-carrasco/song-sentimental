from sqlalchemy.sql.elements import Null
import config.config
from flask import Flask, request , jsonify, render_template
import tools.database as db
from tools.tools import plotsongs, plotartist
import os
from time import sleep
print(" - - - Iniziando API")
app = Flask(__name__, template_folder='templates')
print(" - - - Carga Flask", app)

#////////////////////////////////    GET    /////////////////////////////////////////////////////
 
@app.route("/", methods=["POST", "GET"])
def index():
    return "Index"
                            
@app.route("/songfromid/<id>")
def getsongfromid(id):
    print("- - - Entra en songfromid")
    data=db.get_song_from_id(id)
    return jsonify(data)

@app.route("/allsongs/")
def allsongs():
    print("- - - Entra en allsongs")
    data=db.all_songs()    
    return jsonify(data)

@app.route("/allartists/")
def allartists():
    print("- - - Entra en allsongs")
    data=db.all_artists()    
    return jsonify(data)

@app.route("/songsfromartistid/<id>")
def getsongsfromartistid(id):
    print("- - - Entra en getsongsfromartistid")
    print(id)
    data=db.get_songs_from_artist_id(id)
    return jsonify(data)

@app.route("/songsfromartistname/<name>")
def getsongsfromartistname(name):
    print("- - - Entra en getsongsfromartistname")
    data=db.get_songs_from_artist_name(name)
    return jsonify(data)

@app.route("/lowestcomsong/<n>")
def lowestcomsong(n=None):
    print("- - - Entra en topnegative/<n>")
    data=db.lowest_com_song(n)
    return jsonify(data)

@app.route("/highestcomsong/<n>")
def highestcomsong(n=None):
    data=db.highest_com_song(n)
    return jsonify(data)

@app.route("/countsongsbyartist/")
def countsongsbyartist():
    data=db.count_songs_by_artist()
    return jsonify(data)
#////////////////////////////////    PLOT    /////////////////////////////////////////////////////
@app.route("/plothighestcomsong/<n>", methods=["POST"])
def plothighestcomsong(n=None):
    data=db.highest_com_song(n)
    os.system('rm static/*.png')
    new_graph_name=plotsongs(data)
    h=render_template('output.html',graph=new_graph_name)
    return h
@app.route("/plotartisthist/<name>", methods=["POST"])
def plotartisthist(name):
    data=db.get_songs_from_artist_name(name)
    os.system('rm static/*.png')
    new_graph_name=plotartist(data)
    h=render_template('output.html', graph=new_graph_name)
    return h

#////////////////////////////////    POST    /////////////////////////////////////////////////////
@app.route("/drop", methods=["POST"])
def eliminar():
    print("- - - Entra en drop")
    return db.eliminar()

@app.route("/create", methods=["POST"])
def create():
    print("- - - Entra en create")
    return db.crea()

@app.route("/load", methods=["POST"])
def load():
    print("- - - Entra en load")  
    return db.load()

@app.route("/delete", methods=["POST"])
def delete():
    print("- - - Entra en Delete")
    return db.delete()

@app.route("/newsong", methods=["POST"])
def newsong():
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
    try:
        data = db.intro_artist(artist)
        return jsonify(data)
    except:
        return "error"

@app.route("/deletesongbyid/<id>", methods=["POST"])
def deletesongbyid(id):
    try:
        return db.delete_song_by_id(id)
    except:
        return "error"
   
@app.route("/deleteartisandsongbyidartis/<id>", methods=["POST"])
def deleteartisandsongbyidartis(id):
    try:
        return db.delete_artist_and_song_by_idartist(id)
    except:
        return "error"
    
@app.route("/conectsongartist/", methods=["POST"])
def conectsongartist():
    try:
        id_song=request.args.get("id_song",None)
        id_artist = request.args.get("id_artist", None)
        return db.conect_song_artist(id_song,id_artist)
    except:
        return "error"

app.run("localhost", 5000, debug=True)