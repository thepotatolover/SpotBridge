from pypresence import Presence
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from dotenv import load_dotenv
import os

# Init the .env file and load the things from it
load_dotenv()

discord_client_id = int(os.getenv('discord_client_id'))

username = os.getenv('username')
client_id = os.getenv('spotify_client_id')
client_secret = os.getenv('client_secret')
redirect_uri = os.getenv('redirect_uri')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(username=username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope="user-read-currently-playing"))

def milliseconds_to_minutes_seconds(milliseconds):
    seconds = milliseconds / 1000
    if seconds > 59:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{int(minutes)}:{int(remaining_seconds)}"
    else:
        return f"0:{int(seconds)}"
    
RPC = Presence(discord_client_id,pipe=0)  # Initialize the client class
RPC.connect() # Start the handshake loop

while True:  # The presence will stay on as long as the program is running
    current_track = sp.current_user_playing_track()
    if current_track is not None:
        track_name = current_track['item']['name']
        artist_name = current_track['item']['artists'][0]['name']
        album_name = current_track['item']['album']['name']
        album_image = current_track['item']['album']['images'][0]["url"]
        song_url = current_track['item']['external_urls']['spotify']
        progress = milliseconds_to_minutes_seconds(current_track['progress_ms'])
        duration = milliseconds_to_minutes_seconds(current_track['item']['duration_ms'])
        explict = current_track['item']['explicit']
        if explict == True:
            explict = ', Explict: Yes'
        else:
            explict = ''
        print(RPC.update(details=f"{track_name}, {artist_name}", state=f"{progress}/{duration}{explict}", large_image=album_image, large_text=album_name, buttons=[{"label": "View on Spotify", "url": song_url}, {"label": "GitHub Repo", "url": 'https://github.com/thepotatolover/SpotBridge'}]))
        time.sleep(15) # Can only update rich presence every 15 seconds
    else:
        print(RPC.update(details=f"Not playing"))
        time.sleep(35)
