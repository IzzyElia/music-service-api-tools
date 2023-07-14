import scripts.spotipy_add_artist_to_playlist as add_artists
import scripts.ticketmaster_get_concerts as ticketmaster_concerts
import scripts.utils as utils
import scripts.ticketmaster_api_connector as ticketmaster_api_connector
import scripts.spotipy_api_connector as spotipy_api_connector
import scripts.spotify_get_tracks_of_genre as spotify_get_tracks_of_genre

means_yes = ["yes", "y"]

def idk ():
    print("idk")

def main ():
    utils.restart_log_file()
    methods_dict = {
        "add artist to playlist": add_artists.add_artist,
        "find concerts and shows": ticketmaster_concerts.get_upcoming_concerts,
        "get liked tracks of genre": spotify_get_tracks_of_genre.main,
    }
    while True:
        user_input = input("Welcone to the API Tools. What would you like to do? ")
        utils.quit_check(user_input)
        top_result = utils.fuzzy_sort(list(methods_dict.keys()), user_input)[0]
        method = methods_dict[top_result]
        if input(f"run tool '{top_result}'? (yes/no) ").lower() in means_yes:
            method()

if __name__ == "__main__":
    main()