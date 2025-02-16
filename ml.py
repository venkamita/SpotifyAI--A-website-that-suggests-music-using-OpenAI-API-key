from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from openai import OpenAI
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:5000/callback')

# AI API settings
AI_BASE_URL = os.getenv('AI_BASE_URL', 'https://api.aimlapi.com')
AI_API_KEY = os.getenv('AI_API_KEY')

SCOPE = 'playlist-modify-public playlist-modify-private user-read-private user-read-email'

system_prompt = """
Create a playlist based on mood, artist, genre, and song count.
Return the recommendations in the following format:
1. Song1 by Artist1
2. Song2 by Artist2
3. Song3 by Artist3
"""

api = OpenAI(api_key=AI_API_KEY, base_url=AI_BASE_URL)

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SCOPE
    )

@app.route('/')
def index():
    if not session.get('token_info'):
        return render_template('index.html', logged_in=False)
    return render_template('index.html', logged_in=True)

@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/get_playlist', methods=['POST'])
def get_playlist():
    if not session.get('token_info'):
        return jsonify({"error": "Not logged in"}), 401

    try:
        # Get the user input
        data = request.json
        user_input = data.get("user_input")

        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        # Format the input for the OpenAI API
        formatted_input = f"[{user_input['mood']}, {user_input['artist']}, ({user_input['genre']}), {user_input['numSongs']}]"

        # Get AI recommendations
        logging.debug("Calling OpenAI API...")
        completion = api.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": formatted_input},
            ],
            temperature=0.7,
            max_tokens=256,
        )

        recommendations = completion.choices[0].message.content
        logging.debug(f"AI Recommendations: {recommendations}")

        if not recommendations.strip():
            return jsonify({"error": "No songs recommended by AI"}), 400

        # Create Spotify client
        sp = spotipy.Spotify(auth=session['token_info']['access_token'])
        user_id = sp.current_user()['id']

        # Create a new playlist
        playlist_name = f"AI Generated Playlist - {user_input['mood']}"
        logging.debug(f"Creating playlist: {playlist_name}")
        playlist = sp.user_playlist_create(user_id, playlist_name, public=False)
        playlist_id = playlist['id']

        # Parse the AI recommendations
        songs = recommendations.split('\n')
        track_uris = []

        for song in songs:
            if song.strip():
                # Extract song and artist from the recommendation
                parts = song.split(' by ')
                if len(parts) == 2:
                    track_name = parts[0].split('. ')[-1].strip()
                    artist_name = parts[1].strip()

                    # Search for the track on Spotify
                    query = f"track:{track_name} artist:{artist_name}"
                    logging.debug(f"Searching Spotify for: {query}")
                    result = sp.search(query, type='track', limit=1)

                    if result['tracks']['items']:
                        track_uris.append(result['tracks']['items'][0]['uri'])

        # Add tracks to the playlist
        if track_uris:
            logging.debug(f"Adding {len(track_uris)} tracks to the playlist")
            sp.playlist_add_items(playlist_id, track_uris)
        else:
            return jsonify({"error": "No tracks found on Spotify"}), 404

        # Get the playlist embed URL
        embed_url = f"https://open.spotify.com/embed/playlist/{playlist_id}"
        
        return jsonify({
            "success": True,
            "playlist_id": playlist_id,
            "embed_url": embed_url
        })

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)