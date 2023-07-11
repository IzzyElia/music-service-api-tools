# spotipy_add_artist_to_playlist.py

from scripts.spotipy_api_connector import connect_to_api

def quit_check(user_input):
    if user_input.lower() in ["quit", "q"]:
        print("Exiting program.")
        exit()

def get_artist_tracks(sp, artist_id, featured_only = False, genre = None):
    albums = []
    results = sp.artist_albums(artist_id)
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])

    unique_albums = set()  # To avoid duplicate albums
    tracks = {}

    for album in albums:
        name = album['name']
        print (f"Album: {name}")
        if name not in unique_albums:
            unique_albums.add(name)
            results = sp.album_tracks(album['id'])
            album_tracks = results['items']
            while results['next']:
                results = sp.next(results)
                album_tracks.extend(results['items'])
            for track in album_tracks:
                if featured_only and not any(artist['id'] == artist_id for artist in track['artists']):
                    continue
                tracks[track['id']] = track['name']
                print(f"    - {track['name']}")

    return tracks


def main():
    # Step 1: Connect to the API
    while True:
        try:
            sp = connect_to_api()
            break
        except Exception as e:
            print(e)
            user_input = input("Failed to connect to Spotify API. Try again? (yes/no) ")
            quit_check(user_input)
            if user_input.lower() != "yes":
                return
            continue

    # Step 2: Ask user for an artist to search for
    while True:
        artist_name = input("Enter the name of the artist you're looking for: ")
        quit_check(artist_name)
        results = sp.search(q='artist:' + artist_name, type='artist')
        top_results = results['artists']['items'][:3]

        for i, artist in enumerate(top_results, start=1):
            print(f"Top result {i} for your search is {artist['name']}.")
            user_input = input("Is this the artist you want? (yes/no) ")
            quit_check(user_input)
            if user_input.lower() == "yes":
                artist_id = artist['id']
                break
        else:
            continue
        break

    # Step 3: Ask user for a playlist name to search for or create
    while True:
        playlist_name = input("Enter the name of the playlist: ")
        quit_check(playlist_name)
        user_playlists = sp.current_user_playlists()['items']
        matching_playlists = [pl for pl in user_playlists if playlist_name.lower() in pl['name'].lower()]
        
        if matching_playlists:
            top_result = matching_playlists[0]
            print(f"The top result for your search is {top_result['name']}.")

            user_input = input("Is this the playlist you want? (yes/no) ")
            quit_check(user_input)
            if user_input.lower() == "yes":
                playlist_id = top_result['id']
                break
            user_input = input(f"Do you want to create a new playlist named '{playlist_name}'? (yes/no) ")
            quit_check(user_input)
            if user_input.lower() == "yes":
                user_id = sp.current_user()['id']
                playlist = sp.user_playlist_create(user_id, playlist_name)
                playlist_id = playlist['id']
                print(f"Created playlist named '{playlist_name}'.")
                break
        else:
            print(f"No playlist named '{playlist_name}' found.")
            user_input = input("Do you want to create a new playlist with this name? (yes/no) ")
            quit_check(user_input)
            if user_input.lower() == "yes":
                user_id = sp.current_user()['id']
                playlist = sp.user_playlist_create(user_id, playlist_name)
                playlist_id = playlist['id']
                print(f"Created playlist named '{playlist_name}'.")
                break

    # Step 4: Retrieve all the tracks in the playlist
    tracks_data = sp.playlist_items(playlist_id)
    existing_tracks = {item['track']['id']: item['track']['name'] for item in tracks_data['items']}

    # Step 5: Iterate through all tracks by the selected artist and add them to the playlist
    artist_tracks = get_artist_tracks(sp, artist_id)

    tracks_to_add = [track_id for track_id in artist_tracks.keys() if track_id not in existing_tracks.keys()]

    if tracks_to_add:
        user_input = input(f"Add {len(tracks_to_add)} tracks from {artist_name} to {playlist_name}? (yes/no) ")
        quit_check(user_input)
        if user_input.lower() == "yes":
            # Break the tracks_to_add list into chunks of 100 tracks
            for i in range(0, len(tracks_to_add), 100):
                track_chunk = tracks_to_add[i:i + 100]
                sp.playlist_add_items(playlist_id, track_chunk)
            print("Added new tracks to the playlist.")
        else:
            print("No changes were made to the playlist.")
    else:
        print("No new tracks to add to the playlist.")


    print("Finished managing playlist.")

if __name__ == "__main__":
    main()
