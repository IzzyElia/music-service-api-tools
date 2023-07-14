# spotify_connector.py

import scripts.utils as utils
import os
import configparser
import spotipy
from spotipy.oauth2 import SpotifyOAuth

means_yes = ["yes", "y"]

# Function to create config file
def create_config(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "client_id", "")
    config.set("Settings", "client_secret", "")
    with open(path, "w") as config_file:
        config.write(config_file)

def try_connect_to_spotify(config_file_path = "config/spotify_config.ini"):
    # Connect to the spotify api
    while True:
        try:
            return connect_to_spotify()
            break
        except Exception as e:
            print(e)
            user_input = input("Failed to connect to Spotify API. Try again? (yes/no) ")
            utils.quit_check(user_input)
            if user_input.lower() not in means_yes:
                return
            continue

def connect_to_spotify(config_file_path = "config/spotify_config.ini"):
    # Check if the config file exists. If not, create one.
    if not os.path.exists(config_file_path):
        create_config(config_file_path)
        input("Created config file. Fill it out before continuing")

    # Load the config file
    config = configparser.ConfigParser()
    config.read(config_file_path)

    # Get the values from the config file
    client_id = config.get('Settings', 'client_id')
    client_secret = config.get('Settings', 'client_secret')

    # Authenticate with the Spotify API
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                  client_secret=client_secret,
                                                  redirect_uri="http://localhost:8080/",
                                                  scope="playlist-modify-public playlist-read-private user-library-read",
                                                  cache_path="cache/token_info.txt"))

    # Test API connection by checking current user
    user = sp.current_user()
    if user:
        print(f"Connected to the Spotify API successfully as user {user['display_name']}.")
    else:
        raise Exception("Unable to connect to the Spotify API.")
    return sp
