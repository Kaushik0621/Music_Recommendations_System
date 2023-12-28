import os
import pandas as pd
import config
import numpy as np
import json
import random

training_path = config.training_path
json_path = config.json_path

def convert(o):
    if isinstance(o, np.int64):
        return int(o)
    raise TypeError

def get_user_song_info(user_id, df1, df2):
    dict1 = {}
    index_of_user = df1[df1['user'] == user_id].index.item()
    df1_1 = df1.loc[[index_of_user]].reset_index()
    list1 = []
    song_list_user = []
    for song in df1_1["user_song_info"][0]: song_list_user.append(song[0])
    song_list_user = list(set(song_list_user))
    for x in song_list_user:
        index_of_song = df2[df2['song'] == x].index.item()
        selected_row = df2.iloc[[index_of_song]]
        row_dict = selected_row.to_dict(orient='records')[0]
        row_dict['user_play_count'] = x[1]
        list1.append(row_dict)
    dict1["user"] = user_id
    dict1["user_era"] = df1_1["user_era"][0]
    dict1["data"] = list1
    
    with open(os.path.join(json_path,'user_info.json'), 'w') as json_file:
        json.dump(dict1, json_file, default=convert, indent=2)
    return dict1

def get_song_era_info(song_era, df2):
    list2 = []
    dict2 = {}
    df2_1 = df2.groupby('song_era').agg({'song': list}).reset_index()
    df2_1 = df2_1[df2_1['song_era'] == song_era].reset_index()
    for j in range(len(df2_1)):
        song_list = df2_1['song'][j]
        song_list = list(set(song_list))
        for x in song_list:
            index_of_song = df2[df2['song'] == x].index.item()
            selected_row = df2.iloc[[index_of_song]]
            row_dict = selected_row.to_dict(orient='records')[0]
            list2.append(row_dict)
    list2 = random.sample(list2, min(100, len(list2)))
    dict2["song_era"] = song_era
    dict2["data"] = list2

    with open(os.path.join(json_path,'user_era_song.json'), 'w') as json_file:
        json.dump(dict2, json_file, default=convert, indent=2)
    return dict2

def get_user_top_artist_songs(user_id, df1, df2):
    target_user_data = df1[df1['user'] == user_id].iloc[0]
    artist_play_count = {}
    for song_info in target_user_data['user_song_info']:
        song_id, play_count = song_info
        song_details = df2[df2['song'] == song_id].iloc[0]
        artist_play_count[song_details['artist_name']] = artist_play_count.get(song_details['artist_name'], 0) + play_count
        
        
    sorted_artists = sorted(artist_play_count.items(), key=lambda x: x[1], reverse=True)
    artist_names_only = [artist for artist, _ in sorted_artists]
    users_favourite_artists = artist_names_only[:10] 
    top_artist_songs = {}

    for artist in users_favourite_artists:
        artist_songs = df2[df2['artist_name'] == artist]
        sorted_songs = artist_songs.sort_values(by='play_count', ascending=False)
        top_10_songs = sorted_songs.head(10)
        artist_str = str(artist)
        top_artist_songs[artist_str] = [{
            "song": song['song'],
            "title": song['title'],
            "album": song['release'],
            "artist": song['artist_name']
        } for _, song in top_10_songs.iterrows()]
    dict3 = top_artist_songs
    with open(os.path.join(json_path,'user_top_artist_songs.json'), 'w') as json_file:
        json.dump(dict3, json_file, indent=2)
    return dict3

def get_user_similar_songs(user_id, df1, df2, df3):
    dict4 = {}
    index_of_user = df1[df1['user'] == user_id].index.item()
    df1_1 = df1.loc[[index_of_user]].reset_index()
    list1 = []
    list2 = []
    for x in df1_1["user_song_info"][0]:
        index_of_song = df3[df3['song'] == x[0]].index.item()
        selected_row = df3.iloc[[index_of_song]].reset_index()
        a = [song[0] for song in selected_row["similar_songs"][0]]
        list1.extend([song[0] for song in selected_row["similar_songs"][0]])
        list1 = list(set(list1))
        for x in list1:
            index_of_song = df2[df2['song'] == x].index.item()
            selected_row = df2.iloc[[index_of_song]]
            row_dict = selected_row.to_dict(orient='records')[0]
            list2.append(row_dict)
    dict4["user"] = user_id
    dict4["user_era"] = df1_1["user_era"][0]
    dict4["data"] = list2

    with open(os.path.join(json_path,'user_similar_songs.json'), 'w') as json_file:
        json.dump(dict4, json_file, default=convert, indent=2)
    return dict4

def get_similar_song(song_id, df2, df3):
    dict5 = {}
    list5= []
    index_of_song = df3[df3['song'] == song_id].index.item()
    selected_row = df3.iloc[[index_of_song]].reset_index()
    row_dict = selected_row.to_dict(orient='records')[0]
    for y in row_dict['similar_songs']:
        cosine_similarity = round(y[1], 3)
        index_of_song = df2[df2['song'] == y[0]].index.item()
        selected_row = df2.iloc[[index_of_song]].reset_index()
        selected_row['cosine_similarity'] = cosine_similarity
        index_of_song = df2[df2['song'] == song_id].index.item()
        selected_row1 = df2.iloc[[index_of_song]].reset_index()
        row_dict = selected_row.to_dict(orient='records')[0]
        list5.append(row_dict)
    dict5["song"] = selected_row1['song'][0]
    dict5["title"] = selected_row1['title'][0]
    dict5["play_count"] = selected_row1['play_count'][0]
    dict5["release"] = selected_row1['release'][0]
    dict5["artist_name"] = selected_row1['artist_name'][0]
    dict5["song_era"] = selected_row1['song_era'][0]
    dict5["data"] = list5

    with open(os.path.join(json_path,'user_get_similar_song.json'), 'w') as json_file:
        json.dump(dict5, json_file, default=convert, indent=2)
    return dict5