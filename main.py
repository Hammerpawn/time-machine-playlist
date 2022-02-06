import requests
from bs4 import BeautifulSoup
import os
import spotipy

BILLBOARD_URL = "https://www.billboard.com/charts/hot-100"
CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
REDIRECT_URL = os.environ.get("SPOTIPY_REDIRECT_URL")

while True:
    try:
        date = input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DD: ")
        response = requests.get(f"{BILLBOARD_URL}/{date}")
        response.raise_for_status()
    except requests.HTTPError as exception:
        print("Invalid date. Please try again.")
    else:
        web_page = response.text
        soup = BeautifulSoup(web_page, "html.parser")

        scraped_titles = soup.select("li ul li h3")
        song_list = [song.getText().strip() for song in scraped_titles]
        break

auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URL,
                                           scope="playlist-modify-private")
sp = spotipy.Spotify(auth_manager=auth_manager)

date_year = int(date.split("-")[0])
previous_date_year = date_year - 1
year_range = f"{previous_date_year}-{date_year}"

song_id_list = []
for song in song_list:
    sp_song = sp.search(q=f'{song} year:{year_range}', type='track')
    try:
        song_id = sp_song["tracks"]["items"][0]["id"]
    except IndexError:
        pass
    else:
        song_id_list.append(song_id)

playlist = sp.user_playlist_create(user="applemoose24", name=f"Billboard Top 100 - {date}", public=False)
playlist_id = playlist["id"]
sp.playlist_add_items(playlist_id=playlist_id, items=song_id_list)