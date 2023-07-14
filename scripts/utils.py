import difflib
import os

means_quit = ["quit", "q"]

def quit_check(user_input):
    if user_input.lower() in means_quit:
        print("Exiting program.")
        exit()

def fuzzy_similarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def fuzzy_sort(string_list, query):
    similarity_list = []
    
    for string in string_list:
        similarity = fuzzy_similarity(query, string)
        similarity_list.append((string, similarity))
    
    sorted_list = sorted(similarity_list, key=lambda x: x[1], reverse=True)
    sorted_strings = [string for string, _ in sorted_list]
    
    return sorted_strings

def restart_log_file():
    open("log.txt", "w").close()
    
def log (message):
    #Create the log file if it does not exist
    if not os.path.exists("log.txt"):
        open("log.txt", "w").close()
    log_file = open("log.txt", "a")
    log_file.write(message + "\n")
    log_file.close()