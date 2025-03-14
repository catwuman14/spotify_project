import random
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import config  # Assuming you have a config.py with client_id and client_secret
# Initialize Spotipy with Client Credentials Flow
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.client_id,
                                                           client_secret=config.client_secret))
# Load DataFrames from CSV files
top100 = pd.read_csv("/Users/catherinewu/Downloads/spotify_project/streamlit_top100.csv")
df_combined = pd.read_csv("/Users/catherinewu/Downloads/spotify_project/streamlit_combined.csv")
def play_song(track_id):
    return f"https://open.spotify.com/embed/track/{track_id}"
def fetch_track_id_from_trending(song_title, artist_name):
    search = f"{song_title} - {artist_name}"
    results = sp.search(q=search, limit=1)
    track_id = results["tracks"]["items"][0]["id"]
    return track_id
def recommender():
    genre_to_cluster = {
        "lively": 0,
        "chill": 1,
        "calming": 2,
        "chatty": 3,
        "dramatic": 4,
        "upbeat": 5,
        "instrumental": 6
    }
    valid_genres = list(genre_to_cluster.keys()) + ["trending"]
    st.title("Music Recommender")
    st.write("What music are you in the mood for?")
    st.write(f"Available options: {', '.join(valid_genres)}")
    user_input = st.text_input("Enter a mood for a recommendation (or 'trending'):", "").strip().lower()
    if st.button("Recommend Song"):
        if user_input:
            if user_input == "trending":
                sample = top100.sample(n=1)
                song_title = sample['Title'].values[0]
                artist_name = sample['Artist'].values[0]
                track_id = fetch_track_id_from_trending(song_title, artist_name)
                st.write(f"Playing: {song_title} by {artist_name}")
                st.components.v1.iframe(play_song(track_id), width=320, height=80)
            elif user_input in genre_to_cluster:
                cluster_number = genre_to_cluster[user_input]
                filtered_df = df_combined[df_combined['cluster'] == cluster_number]
                if not filtered_df.empty:
                    random_row = filtered_df.sample(n=1)
                    track_id = random_row['track_id'].values[0]
                    st.write(f"Playing a random {user_input} song")
                    st.components.v1.iframe(play_song(track_id), width=320, height=80)
                else:
                    st.write(f"No songs found for the '{user_input}' mood (cluster {cluster_number}).")
            else:
                st.write(f"'{user_input}' is not a valid option. Please choose from the available moods or 'trending'.")
        else:
            st.write("Please enter a mood or 'trending'.")
if __name__ == "__main__":
    recommender()