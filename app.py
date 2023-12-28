from flask import Flask, render_template, request, jsonify, redirect, url_for
import config
import os
import pandas as pd
import inference
import json
import ast

static_url_path = config.static_url_path
file_path = config.file_path
training_path = config.training_path
json_path = config.json_path
eras = config.era
folder_path = "training/json/era"

df1 = pd.read_csv(os.path.join(training_path, "mapping_user.csv"))
df1["user_song_info"] = df1["user_song_info"].apply(lambda x: ast.literal_eval(x))
df2 = pd.read_csv(os.path.join(training_path, "mapping_song.csv"))
df3 = pd.read_csv("training/mapping_similar_songs.csv")
df3["similar_songs"] = df3["similar_songs"].apply(lambda x: ast.literal_eval(x))

app = Flask(__name__, static_url_path='/static')

def user_info(user_id):
    user_info_dict = inference.get_user_song_info(user_id, df1, df2)
    print("User info received")
    return user_info_dict
def user_similar_songs(user_id):
    user_info_dict = inference.get_user_song_info(user_id, df1, df2)
    print("User info received")
    return user_info_dict

def user_era_song(user_id):
    user_info_dict = user_info(user_id)
    user_era_song_dict = inference.get_song_era_info(int(user_info_dict['user_era']), df2)
    print("User era songs received")
    return user_era_song_dict

def user_top_artist_song(user_id):
    user_top_artist_song_dict = inference.get_user_top_artist_songs(user_id, df1, df2)
    print("User top artists received")
    return user_top_artist_song_dict

def open_json(json_file):
    with open(os.path.join(json_path, json_file), 'r') as json_file:
        data = json.load(json_file)
    return data


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        try: 
            selected_method = request.form.get('inputMethod')
            if selected_method == 'manual':
                user_id = request.form['user_id']
                
            else:
                user_id = request.form['user_id_dropdown']

            if user_id not in list(df1['user']):
                user_not_found = True
                return redirect(url_for('user_not_found', user_id=user_id)) 
            else:
                user_info_data = user_info(user_id)
                user_era_song_data = user_era_song(user_id)
                user_top_artist_song_data = user_top_artist_song(user_id)
                user_similar_songs_data = user_similar_songs(user_id)
                top_songs_era_data = open_json("top_songs_era.json")
                top_songs_data = open_json("top_songs.json")

                return render_template('result.html',
                                   user_id=user_id,
                                   user_info=user_info_data,
                                   user_era_song=user_era_song_data,
                                   user_top_artist_song=user_top_artist_song_data,
                                   user_similar_songs=user_similar_songs_data,
                                   load_all_era_songs=top_songs_era_data,
                                   top_songs=top_songs_data)
        except Exception as e:
            print(f"Error: {e}")

    return render_template('index.html')

@app.route('/user_not_found/<user_id>')
def user_not_found(user_id):
    return render_template('user_not_found.html', user_id=user_id)
@app.route('/category/<category>/<user_id>')
def category(category, user_id):
    data = None
    if category == 'user_info':
        data = open_json("user_info.json")
    elif category == 'user_era_song':
        data = open_json("user_era_song.json")
    elif category == 'user_top_artist_song':
        data = open_json("user_top_artist_songs.json")
    elif category == 'user_similar_songs':
        data = open_json("user_info.json")
    elif category == 'load_all_era_songs':
        data = open_json("top_songs_era.json")
    elif category == 'top_songs':
        data = open_json("top_songs.json")

    return render_template(f'{category}.html', data=data, user_id=user_id)



@app.route('/process_song_selection', methods=['POST'])
def process_song_selection():
    selected_song = request.form.get('song_id_dropdown')
    dict_get_similar_song = inference.get_similar_song(selected_song,df2,df3)
    return render_template('processed_song.html', data= dict_get_similar_song)

@app.route('/selected_song')
def selected_song():

    #song_info = inference.get_song_info(song_id, df2)  # Assuming you have a function to get song info
    data = open_json("user_get_similar_song.json")
    return render_template('selected_song.html', data=data)
if __name__ == '__main__':
    app.run(debug=True)