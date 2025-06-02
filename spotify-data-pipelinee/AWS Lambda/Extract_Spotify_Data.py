import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3 #Communicate to other AWS services
from datetime import datetime

def lambda_handler(event, context):
    client_id = os.environ.get('client_id') #Client ID
    client_secret = os.environ.get('client_secret') #Client Secret

    client_credentials_manager = spotipy.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret) #Authentication 
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    playlist_link = "https://open.spotify.com/playlist/3cEYpjA9oz9GiPac4AsH4n" #SpotifyWebAPI_TestingPlaylist
    playlist_URL = playlist_link.split("/")[-1]

    Siase_spotify_data = sp.playlist_tracks(playlist_URL)
    
    filename = "spotify_raw" + str(datetime.now()) +".json"

    client = boto3.client('s3') #Connect to S3
    client.put_object(
        Body=json.dumps(Siase_spotify_data), 
        Bucket='siase-spotify-pipeline', 
        Key='raw-data/to_process/' + filename) #Upload data to S3 bucket
