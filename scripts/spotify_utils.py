import requests
import time

print_debug_info = False

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
        track_count = 0
        if name not in unique_albums:
            unique_albums.add(name)
            results = sp.album_tracks(album['id'])
            album_tracks = results['items']
            while results['next']:
                results = sp.next(results)
                album_tracks.extend(results['items'])
            for track in album_tracks:
                if not any(artist['id'] == artist_id for artist in track['artists']):
                    continue
                if featured_only and track['artists'][0]['id'] != artist_id:
                    continue
                tracks[track['id']] = track['name']
                track_count += 1
        if print_debug_info and track_count > 0:
            print(f"Found {track_count} tracks in album '{name}'.")

    return tracks

def get_tracks_of_genres(sp, genres):
    tracks = []
    # Get the authentication information from the sp object
    access_token = sp.auth_manager.get_access_token()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    url = "https://api.spotify.com/v1/me/tracks"

    while url:
        response = requests.get(url, headers=headers)
        data = response.json()
        keys = data["items"][0]["track"]["album"].keys()
        for key in keys:
            print(key)
        return

        # If the request was successful, process the tracks
        if response.status_code == 200:
            for item in data['items']:
                # Check if the genres of the track match any of the specified genres
                track_genres = item['track']['genres']
                if any(genre in track_genres for genre in genres):
                    tracks.append(item['track'])

                print(item['track']['name'] + " has genres: " + str(item['track']['genres']))

        # If 400, print the response body then abort
        elif response.status_code == 400:
            print(response.json())
            break
        
        # If rate limited, wait and try again
        elif response.status_code == 429:
            time.sleep(int(response.headers.get('Retry-After', 1)))
            continue

        # If some other error occurred, raise an exception
        else:
            response.raise_for_status()

        # Get the next page of results, or None if this is the last page
        url = data['next']

    return tracks


def get_followed_artists(sp):
    print ("Getting followed artists...")
    artists = []
    results = sp.current_user_followed_artists()
    artists.extend(results['artists']['items'])
    while results['artists']['next']:
        results = sp.next(results['artists'])
        artists.extend(results['artists']['items'])
        if print_debug_info:
            for artist in results['artists']['items']:
                print("Following artist - " + artist['name'])
    return artists