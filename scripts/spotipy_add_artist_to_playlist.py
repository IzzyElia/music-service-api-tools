# spotipy_add_artist_to_playlist.py

from scripts.spotipy_api_connector import try_connect_to_spotify
import random
import scripts.utils as utils
from scripts.spotify_utils import get_artist_tracks

means_yes = ["yes", "y"]
means_all = ["all", "a"]


def add_artist():
    # Step 1: Connect to the API
    sp = try_connect_to_spotify()
    if not sp:
        print("Unable to connect to the Spotify API")
        return

    # Step 2: Ask user for an artist to search for
    while True:
        artist_query = input("Enter the name of the artist you're looking for: ")
        utils.quit_check(artist_query)
        results = sp.search(q='artist:' + artist_query, type='artist')
        top_results = results['artists']['items'][:3]

        for i, artist in enumerate(top_results, start=1):
            print(f"Top result {i} for your search is {artist['name']}.")
            user_input = input("Is this the artist you want? (yes/no) ")
            utils.quit_check(user_input)
            if user_input.lower() in means_yes:
                artist_id = artist['id']
                artist_name = artist['name']
                break
        else:
            continue
        break

    # Step 3: Ask user for a playlist name to search for or create
    while True:
        playlist_name = input("Enter the name of the playlist: ")
        utils.quit_check(playlist_name)
        user_playlists = sp.current_user_playlists()['items']
        matching_playlists = [pl for pl in user_playlists if playlist_name.lower() in pl['name'].lower()]
        
        if matching_playlists:
            top_result = matching_playlists[0]
            print(f"The top result for your search is {top_result['name']}.")

            user_input = input("Is this the playlist you want? (yes/no) ")
            utils.quit_check(user_input)
            if user_input.lower() in means_yes:
                playlist_id = top_result['id']
                break
            user_input = input(f"Do you want to create a new playlist named '{playlist_name}'? (yes/no) ")
            utils.quit_check(user_input)
            if user_input.lower() in means_yes:
                user_id = sp.current_user()['id']
                playlist = sp.user_playlist_create(user_id, playlist_name)
                playlist_id = playlist['id']
                print(f"Created playlist named '{playlist_name}'.")
                break
        else:
            print(f"No playlist named '{playlist_name}' found.")
            user_input = input("Do you want to create a new playlist with this name? (yes/no) ")
            utils.quit_check(user_input)
            if user_input.lower() in means_yes:
                user_id = sp.current_user()['id']
                playlist = sp.user_playlist_create(user_id, playlist_name)
                playlist_id = playlist['id']
                print(f"Created playlist named '{playlist_name}'.")
                break

    # Step 4: Retrieve all the tracks in the playlist
    tracks_data = sp.playlist_items(playlist_id)
    existing_tracks = {item['track']['id']: item['track']['name'] for item in tracks_data['items']}

    # Step 5: Iterate through all tracks by the selected artist and add them to the playlist
    print(f"Searching for tracks by {artist_name}...")
    artist_tracks = get_artist_tracks(sp, artist_id)

    all_non_duplicate_tracks = [track_id for track_id in artist_tracks.keys() if track_id not in existing_tracks.keys()]

    if all_non_duplicate_tracks:
        print (f"Found {len(all_non_duplicate_tracks)} tracks by {artist_name} that are not in the playlist.")
        user_input = input(f"How many tracks do you want to add to {playlist_name}? ('all' to add all) ")
        if user_input.isdigit():
            tracks_to_add = random.sample(all_non_duplicate_tracks, int(user_input))
        elif user_input.lower() in means_all:
            tracks_to_add = all_non_duplicate_tracks
        utils.quit_check(user_input)
        if len(tracks_to_add) > 0:
            # Break the tracks_to_add list into chunks of 100 tracks
            for i in range(0, len(tracks_to_add), 100):
                track_chunk = tracks_to_add[i:i + 100]
                sp.playlist_add_items(playlist_id, track_chunk)
            print(f"Added all tracks by {artist_name} to the playlist.")
        else:
            print("No changes were made to the playlist.")
    else:
        print("No new tracks to add to the playlist.")


    print("Finished managing playlist.")

if __name__ == "__main__":
    add_artist()
