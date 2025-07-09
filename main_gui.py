import PySimpleGUI as sg
from spotify_logic import get_spotify_token, search_for_artist, get_artist_top_tracks
import threading

sg.theme('DarkAmber')

layout = [
    [sg.Text('Artist Name:'), sg.Input(key='-ARTIST_INPUT-')],
    [sg.Button('Search'), sg.Button('Clear')],
    [sg.Text(' ', key='-STATUS-', size=(60, 1))],
    [sg.Multiline(' ', key='-ARTIST_OUTPUT-', size=(80, 20), disabled=True)]
]

window = sg.Window('Spotify Curator', layout, finalize=True)

def search_artist_thread(artist_name, window):
    """Runs the search in a separate thread to prevent GUI freezing."""
    try:
        window['-STATUS-'].update("Getting Spotify token...")
        window.refresh()
        
        token = get_spotify_token()
        if token:
            window['-STATUS-'].update(f"Searching for '{artist_name}'...")
            window.refresh()
            
            artist_data = search_for_artist(token, artist_name)
            if artist_data:
                name = artist_data['name']
                genres = artist_data.get('genres', [])
                popularity = artist_data.get('popularity', 0)
                followers = artist_data.get('followers', {}).get('total', 0)
                
                genres_str = ', '.join(genres) if genres else 'No genres available'
                
                output_text = f"🎵 Artist: {name}\n"
                output_text += f"🎭 Genres: {genres_str}\n"
                output_text += f"📊 Popularity: {popularity}/100\n"
                output_text += f"👥 Followers: {followers:,}\n"
                
                if 'external_urls' in artist_data:
                    spotify_url = artist_data['external_urls'].get('spotify', '')
                    output_text += f"🔗 Spotify URL: {spotify_url}\n"
                
                window['-STATUS-'].update("Getting top tracks...")
                window.refresh()
                
                artist_id = artist_data['id']
                top_tracks_data = get_artist_top_tracks(token, artist_id)
                
                if top_tracks_data and top_tracks_data.get('tracks'):
                    output_text += f"\n🔥 Top 10 Tracks:\n"
                    output_text += "=" * 50 + "\n"
                    
                    for i, track in enumerate(top_tracks_data['tracks'], 1):
                        track_name = track['name']
                        album_name = track['album']['name']
                        track_popularity = track.get('popularity', 0)
                        duration_ms = track.get('duration_ms', 0)
                        
                        # Convert milliseconds to mm:ss format
                        duration_min = duration_ms // 60000
                        duration_sec = (duration_ms % 60000) // 1000
                        duration_str = f"{duration_min}:{duration_sec:02d}"
                        
                        output_text += f"{i:2d}. {track_name}\n"
                        output_text += f"     Album: {album_name}\n"
                        output_text += f"     Popularity: {track_popularity}/100 | Duration: {duration_str}\n"
                        output_text += "-" * 45 + "\n"
                else:
                    output_text += "\n❌ Could not retrieve top tracks.\n"
                
                window['-ARTIST_OUTPUT-'].update(output_text)
                window['-STATUS-'].update("Search completed successfully!")
            else:
                window['-ARTIST_OUTPUT-'].update(f"❌ Artist '{artist_name}' not found.")
                window['-STATUS-'].update("Artist not found.")
        else:
            window['-ARTIST_OUTPUT-'].update("❌ Error: Could not connect to Spotify.")
            window['-STATUS-'].update("Error: Could not get Spotify token.")
    except Exception as e:
        error_msg = f"❌ Error during search: {str(e)}"
        window['-ARTIST_OUTPUT-'].update(error_msg)
        window['-STATUS-'].update("Error occurred during search.")
        print(error_msg)

while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Search':
        artist_name = values['-ARTIST_INPUT-'].strip()
        if artist_name:
            window['-STATUS-'].update("Starting search...")
            window['-ARTIST_OUTPUT-'].update("Searching... Please wait.")
            
            # Run search in a separate thread to prevent GUI freezing
            search_thread = threading.Thread(
                target=search_artist_thread, 
                args=(artist_name, window),
                daemon=True
            )
            search_thread.start()
        else:
            window['-STATUS-'].update("Please enter an artist name.")
    elif event == 'Clear':
        window['-ARTIST_INPUT-'].update('')
        window['-ARTIST_OUTPUT-'].update('')
        window['-STATUS-'].update('')

window.close()