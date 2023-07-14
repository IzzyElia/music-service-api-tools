from scripts.ticketmaster_api_connector import try_get_api_key
from scripts.spotipy_api_connector import try_connect_to_spotify
from scripts.spotify_utils import get_followed_artists
from scripts.utils import quit_check, fuzzy_sort
from datetime import datetime, timedelta
import requests

def get_upcoming_concerts():
    tm_key = try_get_api_key()
    sp = try_connect_to_spotify()
    user_input = input("Enter the name of the city you want to search for: ")
    quit_check(user_input)
    city = user_input

    user_input = input("How many days out do you want to search? (default - 30) ")
    quit_check(user_input)
    if user_input.isnumeric():
        days_in_future = int(user_input)
    else:
        days_in_future = 30

    # Get the users followed artists on spotify
    if sp:
        followed_artists = get_followed_artists(sp)
    else:
        followed_artists = []

    # Get the events near the city, then filter them by the artists the user follows
    url = f"https://app.ticketmaster.com/discovery/v2/events.json"

    # End date for events
    end_date = datetime.now() + timedelta(days=days_in_future)
    end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")  # Format the date as ISO 8601

    # All events
    all_events = []
    all_event_names = []
    page_number = 0
    print (f"Searching for events in {city}...")
    while True:
        querystring = {
            "classificationName":"music",
            "city":city,
            "apikey":tm_key,
            "size":"100", # number of events to retrieve, adjust as necessary
            "endDateTime":end_date_str,
            "page":str(page_number)
        }
        response = requests.get(url, params=querystring)
        data = response.json()
        # Make sure data contains ['_embedded']
        if '_embedded' in data:
            events = data['_embedded']['events']
        # Make sure all_events does not already contain the event
        for event in events:
            if event['name'] not in all_event_names:
                all_events.append(event)
                all_event_names.append(event['name'])

        if int(data['page']['number']) >= int(data['page']['totalPages']):
            break
        page_number += 1

    # The events by artists the user follows
    events_by_followed_artists = []
    # The events by artists the user doesn't follow
    events_by_other_artists = []

    for event in all_events:
        # Check if the event name includes the name of any of the artists the user follows
        if any(artist['name'].lower() in event['name'].lower() for artist in followed_artists):
            events_by_followed_artists.append(event)
        else:
            events_by_other_artists.append(event)

    # Sort the events by date
    events_by_followed_artists.sort(key=lambda event: event['dates']['start']['localDate'])
    events_by_other_artists.sort(key=lambda event: event['dates']['start']['localDate'])

    print ("\nEvents by artists followed---------------------")
    for event in events_by_followed_artists:
        print(f"{event['name']} on {event['dates']['start']['localDate']} at {event['_embedded']['venues'][0]['name']}")

    print (f"\nSee output/events.txt for all events in {city}---------------------")

    events_file = open("output/events.txt", "w")
    events_file.write("Events by followed artists---------------------\n")
    for event in events_by_followed_artists:
        events_file.write(f"{event['name']} on {event['dates']['start']['localDate']} at {event['_embedded']['venues'][0]['name']}\n")

    events_file.write("\n\n\nAll events---------------------\n")
    for event in all_events:
        events_file.write(f"{event['name']} on {event['dates']['start']['localDate']} at {event['_embedded']['venues'][0]['name']}\n")
