import json
import boto3
import pandas as pd
from datetime import datetime
from io import StringIO


def album(data):
    items_data = data["items"]
    album_list = []
    for row in items_data:
        album_id = row["track"]["album"]["id"]
        album_name = row["track"]["album"]["name"]
        album_release_date = row["track"]["album"]["release_date"]
        album_total_tracks = row["track"]["album"]["total_tracks"]
        album_external_urls = row["track"]["album"]["external_urls"]["spotify"]
        all_info = {"album_id":album_id,"album_name":album_name,"album_release":album_release_date,"album_total_tracks":album_total_tracks,
                "album_external_urls":album_external_urls}
        album_list.append(all_info)
    return album_list


def artist(data):
    items_data = data["items"]
    artist_list = [] 
    for row in items_data:
        for key,value in row.items():  #row.items() is used to get inside the [] of items(items_data) so we can then access the dictionary{} 
            if key == "track":
                for artist in value["artists"]: #same as above comment. Need to loop again to get inside the [] to access {}dictionary instead of list[].
                    artist_dictionary = {"artist_id":artist["id"], "artist_name":artist["name"], "external_url": artist["href"]}
                    artist_list.append(artist_dictionary)
    return artist_list

def songs(data):
    song_list = []
    items_data = data["items"]
    for row in items_data:
        song_id = row["track"]["id"]
        song_name = row["track"]["name"]
        song_duration = row["track"]["duration_ms"]
        song_url = row["track"]["external_urls"]["spotify"]
        song_popularity = row["track"]["popularity"]
        song_added = row["added_at"]
        album_id = row["track"]["album"]["id"]
        artist_id = row["track"]["album"]["artists"][0]["id"]
        song_element = {"song_id":song_id, "song_name":song_name, "song_duration":song_duration,"song_url":song_url,"song_popularity":song_popularity,
        "song_added":song_added, "album_id":album_id, "artist_id":artist_id}
        song_list.append(song_element)
    return song_list
    


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    Bucket = "siase-spotify-pipeline"
    key = "raw-data/to_process/"

    spotify_data = []
    spotify_key = []
    for file in s3.list_objects(Bucket=Bucket, Prefix=key)["Contents"]:
        file_key = file["Key"]
        if file_key.split(".")[-1] == "json":
            response = s3.get_object(Bucket=Bucket, Key=file_key)
            content = response["Body"]
            jsonObject = json.loads(content.read())
            spotify_data.append(jsonObject)
            spotify_key.append(file_key)
    for data in spotify_data:
        album_list = album(data)
        artist_list = artist(data)
        song_list = songs(data)

        album_df = pd.DataFrame(album_list)
        album_df = album_df.drop_duplicates(subset=["album_id"])

        artist_df = pd.DataFrame(artist_list)
        artist_df = artist_df.drop_duplicates(subset=["artist_id"])

        song_df = pd.DataFrame(song_list)  
        album_df["album_release"] = pd.to_datetime(album_df["album_release"])
        song_df["song_added"] = pd.to_datetime(song_df["song_added"])      

        songs_key = "transform-data/songs_data/songs_transformed_" + str(datetime.now()) + ".csv"
        song_buffer=StringIO()
        song_df.to_csv(song_buffer, index=False) # False means you’re not including the DataFrame’s row numbers in the CSV
        song_content = song_buffer.getvalue()
        s3.put_object(Bucket=Bucket, Key=songs_key, Body=song_content)
        
        album_key = "transform-data/album_data/album_transformed_" + str(datetime.now()) + ".csv"
        album_buffer=StringIO()
        album_df.to_csv(album_buffer, index=False)
        album_content = album_buffer.getvalue()
        s3.put_object(Bucket=Bucket, Key=album_key, Body=album_content)
        
        artist_key = "transform-data/artist_data/artist_transformed_" + str(datetime.now()) + ".csv"
        artist_buffer=StringIO()
        artist_df.to_csv(artist_buffer, index=False)
        artist_content = artist_buffer.getvalue()
        s3.put_object(Bucket=Bucket, Key=artist_key, Body=artist_content)

    s3_resource = boto3.resource('s3')
    for key in spotify_key:
        copy_source = {
        'Bucket': Bucket,
        'Key': key
        }
        s3_resource.meta.client.copy(copy_source, Bucket, 'raw-data/processed/' + key.split("/")[-1])    
        s3_resource.Object(Bucket, key).delete()            
            
        
