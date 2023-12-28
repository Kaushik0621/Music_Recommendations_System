import os
import pandas as pd
import json
import config
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def train_data():
    # Set the file paths for input CSV and output directories
    file_path = config.file_path
    training_path = config.training_path
    if not os.path.exists(training_path): os.makedirs(training_path)

    # Set the path for the 'json' directory inside 'training'
    json_path = config.json_path
    if not os.path.exists(json_path): os.makedirs(json_path)

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Create a new column 'song_era' by grouping years into intervals of 5
    df['song_era'] = df['year'].apply(lambda x: (x // 5) * 5)

    # Drop unnecessary columns from the DataFrame
    df_song = df.drop(["year", "user"], axis=1)

    # Call the 'mapping_song' function
    mapping_song_df = mapping_song(df_song, training_path)

    # Call the 'mapping_user' function
    mapping_user(df, training_path)

    # Call the 'dict_top_songs' function to create a JSON file for top songs
    dict_top_songs(df_song, json_path)

    # Call the 'dict_top_songs_era' function to create JSON files for top songs by era
    dict_top_songs_era(mapping_song_df, json_path)

    # THIS FILE WILL TAKE 1 HOUR TO TRAIN, UNCOMMENT THIS LINE BELOW TO TRAIN AGAIN
    # mapping_song_cosine_similarity(mapping_song_df, training_path)

    print("Data trained!")
    return training_path

def mapping_song(df_song, training_path):
    # Group by 'song' and aggregate play counts, selecting additional information
    sum_play_count_by_song = df_song.groupby('song').agg({'play_count': 'sum', 'title': 'first', 'release': 'first', 'artist_name': 'first', 'song_era': 'first'}).reset_index()

    # Save the mapping to a CSV file
    sum_play_count_by_song.to_csv(os.path.join(training_path, "mapping_song.csv"), index=False)

    return sum_play_count_by_song

def mapping_user(df, training_path):
    # Extract relevant columns and filter out rows with 'song_era' equal to 0
    df_user = df[["user", "song_era"]]
    filtered_df = df_user[df_user['song_era'] != 0]

    # Group by 'user' and calculate the mean of 'song_era', creating a new column 'user_era'
    average_era_by_user = filtered_df.groupby('user')['song_era'].mean().reset_index()
    average_era_by_user['user_era'] = average_era_by_user['song_era'].apply(lambda x: int((x // 5) * 5))
    average_era_by_user = average_era_by_user.drop("song_era", axis=1)

    # Calculate the mean of 'user_era' and create a missing user with the calculated era
    user_era_mean = int((average_era_by_user["user_era"].mean() // 5) * 5)
    missing_user = {'user': '07468cd3a1d3a119f1769eeae2b34aaebc096ec2', 'user_era': user_era_mean}
    average_era_by_user = pd.concat([average_era_by_user, pd.DataFrame([missing_user])], ignore_index=True)

    # Drop unnecessary columns and create a new column 'user_song_info'
    df_new = df.drop(["title", "release", "artist_name", "year"], axis=1)
    df_new['user_song_info'] = df_new.apply(lambda row: (row['song'], row['play_count']), axis=1)

    # Group by 'user' and aggregate the 'user_song_info' column as a list
    df_new1 = df_new.groupby('user').agg({'user_song_info': list}).reset_index()

    # Merge the DataFrames and save the mapping to a CSV file
    merged_df = pd.merge(average_era_by_user, df_new1, on='user', how='inner')
    merged_df.to_csv(os.path.join(training_path, "mapping_user.csv"), index=False)

def dict_top_songs(df_mapping_song, json_path):
    # Sort the DataFrame by 'play_count' in descending order and select the top 100 rows
    df_top_songs = df_mapping_song.sort_values(by='play_count', ascending=False).head(100)
    top_songs_info = df_top_songs[['song', 'title', 'artist_name', 'play_count', 'release', 'song_era']]

    # Convert the top songs information to a dictionary
    top_songs_dict = {"file_name": "top_songs.json", "data": top_songs_info.to_dict(orient='records')}

    # Set the path for the top songs JSON file
    json_file_path = os.path.join(json_path, "top_songs.json")

    # Save the top songs dictionary as a JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(top_songs_dict, json_file, indent=2)

    # print(f"Top songs JSON file saved at: {json_file_path}")

def dict_top_songs_era(df2, json_path):
    
    dict_top_songs_era = {}
    filtered_df_1950 = df2[df2['song_era'].isin([1950, 1955])].sort_values(by='play_count', ascending=False).reset_index(drop=True)
    dict_top_songs_era['1950'] = filtered_df_1950.head(20).to_dict(orient='records')
    filtered_df_1960 = df2[df2['song_era'].isin([1960, 1965])].sort_values(by='play_count', ascending=False).reset_index(drop=True)
    dict_top_songs_era['1960'] = filtered_df_1960.head(20).to_dict(orient='records')
    filtered_df_1970 = df2[df2['song_era'].isin([1970, 1975])].sort_values(by='play_count', ascending=False).reset_index(drop=True)
    dict_top_songs_era['1970'] = filtered_df_1970.head(20).to_dict(orient='records')
    filtered_df_1980 = df2[df2['song_era'].isin([1980, 1985])].sort_values(by='play_count', ascending=False).reset_index(drop=True)
    dict_top_songs_era['1980'] = filtered_df_1980.head(20).to_dict(orient='records')
    filtered_df_1990 = df2[df2['song_era'].isin([1990, 1995])].sort_values(by='play_count', ascending=False).reset_index(drop=True)
    dict_top_songs_era['1990'] = filtered_df_1990.head(20).to_dict(orient='records')
    filtered_df_2000 = df2[df2['song_era'].isin([2000, 2005])].sort_values(by='play_count', ascending=False).reset_index(drop=True)
    dict_top_songs_era['2000'] = filtered_df_2000.head(20).to_dict(orient='records')
    filtered_df_2010 = df2[df2['song_era'].isin([2010])].sort_values(by='play_count', ascending=False).reset_index(drop=True)
    dict_top_songs_era['2010'] = filtered_df_2010.head(20).to_dict(orient='records')

    for key in ['1950','1960','1970','1980','1990','2000','2010']: dict_top_songs_era[key] = dict_top_songs_era.pop(key)
    with open(os.path.join(json_path, "top_songs_era.json"), 'w') as json_file:
                    json.dump(dict_top_songs_era, json_file, indent=2)
 
    print("All JSON files created and saved.")

def mapping_song_cosine_similarity(df2, training_path):
    df3 = pd.DataFrame(df2)

    # TF-IDF Vectorization
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df3['title'])
    # Calculate cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    # Create a DataFrame for cosine similarity
    cosine_sim_df = pd.DataFrame(cosine_sim, columns=df3['song'], index=df3['song'])

    # Create a list to store the data for the new DataFrame
    similar_songs_data = []

    # Iterate through each song
    for song in df3['song']:
        # Get the cosine similarity scores for the current song
        similar_scores = cosine_sim_df[song]
        # Sort the scores in descending order
        sorted_scores = similar_scores.sort_values(ascending=False)
        # Exclude the input song itself
        sorted_scores = sorted_scores.drop(song)
        # Get the top 5 most similar songs
        top_similar_songs = list(sorted_scores.index[:5])
        # Combine song names with their similarity scores
        similar_songs_info = list(zip(top_similar_songs, sorted_scores[top_similar_songs]))
        # Append to the list
        similar_songs_data.append({'song': song, 'similar_songs': similar_songs_info})
    # Create the new DataFrame
    similar_songs_df = pd.DataFrame(similar_songs_data)

    # Display the resulting DataFrame
    similar_songs_df.to_csv(os.path.join(training_path, "mapping_similar_songs.csv"), index=False)


    
train_data()
