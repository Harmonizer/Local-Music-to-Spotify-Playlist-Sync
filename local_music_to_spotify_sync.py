import os
from mutagen import File
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
client_id = ""
client_secret = ""
redirect_uri = "https://localhost:8080"
scope = "playlist-modify-private"
username = ""
playlist_id = ''

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

audio_metadata_list = []
found_track_list_uri = []

def list_audio_files_in_directory(directory):
    """
    List audio files in the specified directory and extract their metadata.
    
    Args:
        directory (str): Path to the directory containing audio files.
    
    Returns:
        list: List of audio file metadata strings.
    """
    audio_extensions = {'.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma'}
    print(f"\nFiles with unknown metadata in '{directory}': \n-------------------------------------------------------------------")
    metadata = []

    try:
        files = os.listdir(directory)
        for file in files:
            full_path = os.path.join(directory, file)
            if os.path.isfile(full_path) and os.path.splitext(file)[1].lower() in audio_extensions:
                file_metadata = get_audio_metadata(full_path)
                if file_metadata:
                    metadata.append(file_metadata)
                else:
                    print(f"{file}")
        
        print_metadata_summary(directory, metadata)
    except FileNotFoundError:
        print(f"The directory '{directory}' does not exist.")
    except PermissionError:
        print(f"Permission denied for accessing the directory '{directory}'.")

    return metadata

def get_audio_metadata(file_path):
    """
    Extract metadata from an audio file.
    
    Args:
        file_path (str): Path to the audio file.
    
    Returns:
        str: Formatted string with artist and title, or None if metadata is missing.
    """
    metadata = {"title": "Unknown Title", "artist": "Unknown Artist"}
    try:
        audio = File(file_path, easy=True)
        if audio is not None:
            metadata['title'] = audio.get('title', ["Unknown Title"])[0]
            metadata['artist'] = audio.get('artist', ["Unknown Artist"])[0]
            if metadata['title'] != "Unknown Title" and metadata['artist'] != "Unknown Artist":
                track_info = f"{metadata['artist']} - {metadata['title']}"
                audio_metadata_list.append(track_info)
                return track_info
    except Exception as e:
        print(f"Error reading metadata for {os.path.basename(file_path)}: {e}")
    return None

def print_metadata_summary(directory, metadata):
    """
    Print a summary of the audio file metadata.
    
    Args:
        directory (str): Path to the directory containing audio files.
        metadata (list): List of metadata strings for the audio files.
    """
    if metadata:
        print(f"\n\nMusic tracks in '{directory}':\n-------------------------------------------------")
        for index, track in enumerate(metadata, start=1):
            print(f"{index}. {track}")
        print("\n")
    else:
        print(f"No audio files found in '{directory}' with known metadata.")

def search_spotify():
    """
    Search for each track in the audio_metadata_list on Spotify and collect their URIs.
    """
    print(f"Spotify search results:\n--------------------------")
    
    for index, track in enumerate(audio_metadata_list, start=1):
        results = sp.search(q=track, limit=1, market='NL')
        if results['tracks']['items']:
            title = results['tracks']['items'][0]['name']
            artist = results['tracks']['items'][0]['artists'][0]['name']
            track_uri = results['tracks']['items'][0]['uri']
            track_entry = f"{index}. {track_uri} : {artist} - {title}"
            
            print(track_entry)
            found_track_list_uri.append(track_uri)
        else:
            print(f'{index}. No tracks found for "{track}".')

    print("\n")

def populate_playlist(show_old_playlist=False, show_new_playlist=False):
    """
    Populate the Spotify playlist with tracks found in the search.
    
    Args:
        show_old_playlist (bool): Whether to display the current playlist contents.
        show_new_playlist (bool): Whether to display the updated playlist contents.
    """
    tracks = found_track_list_uri
    
    if show_old_playlist:
        display_playlist_contents(playlist_id, "Current playlist")
    
    update_playlist(playlist_id, tracks)
    
    if show_new_playlist:
        display_playlist_contents(playlist_id, "Updated playlist")

def display_playlist_contents(playlist_id, title):
    """
    Display the contents of a Spotify playlist.
    
    Args:
        playlist_id (str): Spotify playlist ID.
        title (str): Title to display above the playlist contents.
    """
    offset = 0
    print(f"{title}:\n-----------------")
    
    while True:
        response = sp.playlist_items(playlist_id, offset=offset, market='NL', fields='items.track.artists.name,items.track.name,total', additional_types=['track'])
        if len(response['items']) == 0:
            break
        
        for index, item in enumerate(response['items']):
            print(f"{offset + index + 1} {item['track']['artists'][0]['name']} - {item['track']['name']}")
        
        offset += len(response['items'])
        print(f"[{offset} / {response['total']}]\n")

def update_playlist(playlist_id, tracks):
    """
    Update the Spotify playlist with the given tracks, removing duplicates first.
    
    Args:
        playlist_id (str): Spotify playlist ID.
        tracks (list): List of Spotify track URIs to add to the playlist.
    """
    for i in range(0, len(tracks), 20):
        chunk = tracks[i:i + 20]
        sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, chunk)
        sp.user_playlist_add_tracks(username, playlist_id, chunk)

if __name__ == "__main__":
    # Directory path input
    directory_path = input("Enter the directory path: ")

    # Get list of audio files with metadata
    list_audio_files_in_directory(directory_path)
    
    # Search Spotify for the audio files
    search_spotify()
    
    # Populate the Spotify playlist with found tracks
    # Set show_old_playlist and show_new_playlist to True or False as needed
    populate_playlist(show_old_playlist=False, show_new_playlist=True)
