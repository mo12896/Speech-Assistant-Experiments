import speech_recognition as sr
import pyttsx3
import pyaudio
import pywhatkit
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from datetime import datetime
import wikipedia
import pyjokes
import requests
import json
import gmaps
from twilio.rest import Client


listener = sr.Recognizer()
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

# Google-Maps
gmaps.configure(api_key="Your api key here")

# Whatsapp
account_sid = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
auth_token = "your_auth_token"
client = Client(account_sid, auth_token)

# Spotify
scope = "user-read-playback-state,user-modify-playback-state"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id="...",
        client_secret="...",
        redirect_uri="http://example.com/",
        scope=scope,
    )
)
spotify_albums = {}


def spotify_player(artist_name, track_name):
    artist_name = artist_name
    track_name = track_name
    _, album_uris = get_album_uris(artist_name)

    for i in album_uris:  # each album
        x = albumSongs(i, track_name)
        # print(x)
        if x != None:
            artist_song = x

    sp.start_playback(uris=[artist_song])


def albumSongs(uri, track_name):
    album = uri  # assign album uri to a_name

    spotify_albums[album] = {}  # Creates dictionary for that specific album
    spotify_albums[album]["name"] = []
    spotify_albums[album]["uri"] = []

    tracks = sp.album_tracks(album)  # pull data on album tracks

    for n in range(len(tracks["items"])):  # for each song track
        # print(tracks['items'][n]['name'])
        if track_name == tracks["items"][n]["name"]:
            song = tracks["items"][n]["uri"]
            return song


def get_album_uris(artist_name):
    artist_name = artist_name
    # results = sp.search(q='track:' + name, type='track')
    result = sp.search(artist_name)
    # Extract Artist's uri
    artist_uri = result["tracks"]["items"][0]["artists"][0]["uri"]
    # Pull all of the artist's albums
    sp_albums = sp.artist_albums(artist_uri, album_type="album")
    # Store artist's albums' names' and uris in separate lists
    album_names = []
    album_uris = []
    for i in range(len(sp_albums["items"])):
        album_names.append(sp_albums["items"][i]["name"])
        album_uris.append(sp_albums["items"][i]["uri"])
    return album_names, album_uris


# spotify_player('Coldplay', 'Viva La Vida')


def get_weather(city):
    # Enter your API key here
    api_key = "Your_API_Key"

    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?q="

    # Give city name
    city_name = city

    # complete_url variable to store
    # complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":
        # store the value of "main"
        # key in variable y
        y = x["main"]

        # store the value corresponding
        # to the "temp" key of y
        current_temperature = y["temp"]

        # store the value corresponding
        # to the "pressure" key of y
        current_pressure = y["pressure"]

        # store the value corresponding
        # to the "humidity" key of y
        current_humidiy = y["humidity"]

        # store the value of "weather"
        # key in variable z
        z = x["weather"]

        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]

        return (
            current_temperature,
            current_pressure,
            current_humidiy,
            weather_description,
        )

    else:
        print(" City Not Found ")


def send_message(name, message):
    number = get_number(name)
    message = client.messages.create(
        from_="whatsapp:+15122443225", body=message, to="whatsapp:" + number
    )


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    # try:
    with sr.Microphone(device_index=3) as source:
        # listener.adjust_for_ambient_noise(source)
        print("listening ...")
        voice = listener.listen(source)
        command = listener.recognize_google(voice)
        command = command.lower()
        if "alexa" in command:
            command = command.replace("alexa", "")
    # except:
    #    pass
    return command


def run_alexa():
    command = take_command()
    # command = command.split()
    print(command)
    if "play" in command:
        # Alexa, play song of artist
        song_in = command.replace("play ", "")
        x = song_in.split(" off", 1)
        artist = x[1].replace(" ", "", 1)
        song = x[0].replace(" ", "", 1)
        artist = artist.title()
        song = song.title()
        print(artist, song)
        talk("I play the song {} of {}".format(song, artist))
        spotify_player(artist, song)
    elif "time" in command:
        time = datetime.today().strftime("%H:%M")
        print(time)
        talk("Current time is " + time)
    elif "date" in command:
        date = datetime.today().strftime("%x")
        print(date)
        talk("Current date is " + date)
    elif "show" in command:
        video = command.replace("show", "")
        talk("show " + video + " on youtube")
        pywhatkit.playonyt(video)
    elif "weather" in command:
        word_list = command.split()
        city = word_list[-1]
        temp, atm, hum, descr = get_weather(city)
        talk()
    elif "who is" or "what is" in command:
        if "who is" in command():
            thing = command.replace("who is", "")
        else:
            thing = command.replace("what is", "")
        info = wikipedia.summary(thing, 1)
        print(info)
        talk(info)
    elif "distance" in command():
        pass
    elif "joke" in command():
        talk(pyjokes.get_joke())
    elif "message" in command():
        pass
    else:
        talk("Please say the command again!")


if __name__ == "__main__":
    while True:
        run_alexa()

