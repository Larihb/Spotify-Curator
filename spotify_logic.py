import os
import base64
import requests
from dotenv import load_dotenv
import subprocess
import json

load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_spotify_token():
    """Gets Spotify access token using curl to avoid environment issues."""
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    
    curl_command = [
        'curl', '-X', 'POST', 'https://accounts.spotify.com/api/token',
        '-H', f'Authorization: Basic {auth_base64}',
        '-H', 'Content-Type: application/x-www-form-urlencoded',
        '-d', 'grant_type=client_credentials'
    ]
    
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and result.stdout:
            try:
                json_response = json.loads(result.stdout)
                return json_response.get('access_token')
            except json.JSONDecodeError:
                print("Error: Could not decode JSON response from curl.")
                print("Raw response:", result.stdout)
                return None
        else:
            print("Error executing curl command.")
            print("Return code:", result.returncode)
            print("Stderr:", result.stderr)
            return None
    except subprocess.TimeoutExpired:
        print("Error: Curl command timed out.")
        return None
    except Exception as e:
        print(f"Error executing curl command: {e}")
        return None

def search_for_artist(token, artist_name):
    """Searches for an artist on Spotify."""
    SEARCH_URL = "https://api.spotify.com/v1/search"
    headers = {
        'Authorization': f"Bearer {token}"
    }
    params = {
        'q': artist_name,
        'type': 'artist',
        'limit': 1
    }
    
    try:
        response = requests.get(SEARCH_URL, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            search_results = response.json()
            if search_results['artists']['items']:
                return search_results['artists']['items'][0]
            return None
        else:
            print(f"Search error - Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

def get_artist_top_tracks(token, artist_id):
    """Gets an artist's top 10 tracks."""
    TOP_TRACKS_URL = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = {
        'Authorization': f"Bearer {token}"
    }
    params = {
        'market': 'BR'
    }
    
    try:
        response = requests.get(TOP_TRACKS_URL, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            # Ensure maximum 10 tracks
            if 'tracks' in data:
                data['tracks'] = data['tracks'][:10]
            return data
        else:
            print(f"Top tracks error - Status Code: {response.status_code}")
            return {"tracks": []}
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return {"tracks": []}

def get_audio_features_for_tracks(token, track_ids):
    """Gets audio features for multiple tracks."""
    FEATURES_URL = "https://api.spotify.com/v1/audio-features"
    headers = {
        'Authorization': f"Bearer {token}"
    }
    params = {
        'ids': ",".join(track_ids)
    }
    
    try:
        response = requests.get(FEATURES_URL, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            return response.json().get('audio_features', [])
        else:
            print(f"Audio features error - Status Code: {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []