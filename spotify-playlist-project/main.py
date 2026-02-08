import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("client_secret")
REDIRECT_URL = "https://example.com"
token = os.getenv("TOKEN")



user_choice = input("Which year do you want to travel to? Type the data in this format YYYY-MM-DD: ")

header = {"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"}
billbord_url = f"https://www.billboard.com/charts/hot-100/{user_choice}/"

response = requests.get(url=billbord_url)
songs_data = response.text

soup = BeautifulSoup(songs_data, "lxml")
# song_names_spans = soup.select("li ul li h3")
# song_names = [song.getText().strip() for song in song_names_spans]

songs_list = soup.find_all(name="h3", class_="c-title a-font-basic u-letter-spacing-0010 u-max-width-397"
                                             " lrv-u-font-size-16 lrv-u-font-size-14@mobile-max u-line-height-22px"
                                             " u-word-spacing-0063 u-line-height-normal@mobile-max"
                                             " a-truncate-ellipsis-2line lrv-u-margin-b-025"
                                             " lrv-u-margin-b-00@mobile-max")
songs_names = [song_info.getText().strip() for song_info in songs_list]
scope = "playlist-modify-private"


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                                               redirect_uri=REDIRECT_URL,scope=scope))
access_token = sp.auth_manager.get_access_token(as_dict=False)
user_id = sp.current_user()["id"]


songs_uri = []


for song in songs_names:
    try:
        result = sp.search(q=f"track:{song} year:{user_choice.split('-')[0]}", type="track", limit=1)
        songs_uri.append(result["tracks"]["items"][0]["uri"])
    except IndexError:
        pass


new_playlist = sp.user_playlist_create(user=user_id,name=F"{user_choice} Billboard 100",public=False)
new_playlist_id = new_playlist["id"]


add_tracks = sp.playlist_add_items(playlist_id=new_playlist_id, items=songs_uri)















