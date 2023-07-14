# ticketmaster_api_connector.py

import os
import configparser
import requests

means_yes = ["yes", "y"]

# Function to create config file
def create_config(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "api_key", "")
    with open(path, "w") as config_file:
        config.write(config_file)

def try_get_api_key(config_file_path = "config/ticketmaster_config.ini"):
    # Get the ticketmaster api key
    while True:
        try:
            return get_ticketmaster_api_key(config_file_path)
            break
        except Exception as e:
            print(e)
            user_input = input("Failed to connect to Ticketmaster API. Try again? (yes/no) ")
            utils.quit_check(user_input)
            if user_input.lower() not in means_yes:
                return

def get_ticketmaster_api_key(config_file_path = "config/ticketmaster_config.ini"):
    # Check if the config file exists. If not, create one.
    if not os.path.exists(config_file_path):
        create_config(config_file_path)
        input("Created config file. Fill it out before continuing")

    # Load the config file
    config = configparser.ConfigParser()
    config.read(config_file_path)

    # Get the values from the config file
    api_key = config.get('Settings', 'api_key')

    # Check if the API key is valid by making a simple request
    response = requests.get(f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={api_key}&size=1")

    if response.status_code == 200:
        print("Connected to the Ticketmaster API successfully.")
    else:
        raise Exception("Unable to connect to the Ticketmaster API.")
    
    return api_key
