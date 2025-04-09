from flask import Flask, redirect, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv() 

# Initialize the Flask app
app = Flask(__name__)

# Set up Spotify API credentials and redirect URI
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')  # Example: 'http://localhost:5000/callback'
SCOPE = 'user-top-read user-library-read'

print(f"CLIENT_ID: {CLIENT_ID}")
print(f"CLIENT_SECRET: {CLIENT_SECRET}")
print(f"REDIRECT_URI: {REDIRECT_URI}")

# Initialize Spotipy with OAuth manager
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=REDIRECT_URI,
                                                scope=SCOPE))

@app.route('/')
def home():
    return 'Welcome to your Spotify Wrapped App!'

# Step 1: Redirect to Spotify login page
@app.route('/login')
def login():
    auth_url = sp.auth_manager.get_authorize_url()
    return redirect(auth_url)

# Step 2: Callback from Spotify after login
@app.route('/callback')
def callback():
    # Retrieve the access token from Spotify
    token_info = sp.auth_manager.get_access_token(request.args['code'])
    sp.auth_manager.cache_token(token_info)
    return jsonify(token_info)

# Step 3: Display the user's top tracks
@app.route('/top-tracks')
def top_tracks():
    # Retrieve top tracks of the user (can specify the number of tracks)
    results = sp.current_user_top_tracks(limit=10, offset=0, time_range='medium_term')  # Can be 'short_term', 'medium_term', 'long_term'
    top_tracks = results['items']
    
    # Format the response to include track name and artist name
    tracks_info = [{'name': track['name'], 'artist': track['artists'][0]['name']} for track in top_tracks]
    
    return jsonify(tracks_info)

if __name__ == '__main__':
    app.run(debug=True)
