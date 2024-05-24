# Local Music to Spotify Playlist Sync

## Overview
**Local Music to Spotify Playlist Sync** is a Python script created to run on a Windows machine. It helps users sync their local music files with a Spotify playlist. The script is currently tailored to support a directory containing individual tracks, mimicking the structure of an old MP3 player.

It automates the process of scanning a directory for audio files, extracting their metadata, searching for these tracks on Spotify, and updating a specified Spotify playlist with the found tracks.

## Features
- **Metadata Extraction**: Scans a specified directory for audio files and extracts metadata (artist and title).
- **Spotify Search**: Searches Spotify for each track using the extracted metadata.
- **Playlist Update**: Adds the found tracks to a specified Spotify playlist, removing any duplicates beforehand.
- **Playlist Display Options**: Optionally displays the contents of the playlist before and after the update.

## Problem It Solves
Manually managing and syncing local music files with a Spotify playlist can be time-consuming and error-prone. This script automates the process, ensuring that your Spotify playlist reflects the music you have locally, complete with accurate metadata matching.

## Requirements
- Python 3.x
- [spotipy](https://spotipy.readthedocs.io/en/2.19.0/)
- [mutagen](https://mutagen.readthedocs.io/en/latest/)

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/local-music-to-spotify-sync.git
   cd local-music-to-spotify-sync
   
## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## Contact
For any questions or feedback, please contact harmonizer@unsaved.work.
