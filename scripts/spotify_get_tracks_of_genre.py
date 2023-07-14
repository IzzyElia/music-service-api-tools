import scripts.spotify_utils as spotify_utils
import scripts.spotipy_api_connector as spotipy_api_connector
import scripts.utils as utils

def main():
    sp = spotipy_api_connector.try_connect_to_spotify()
    if not sp:
        print("Unable to connect to the Spotify API")
        return
    
    user_input = input("Enter the genre you're looking for: ")
    utils.quit_check(user_input)
    tracks = spotify_utils.get_tracks_of_genres(sp, user_input)
    print(tracks)