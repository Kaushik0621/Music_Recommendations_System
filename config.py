import os

cwd = os.getcwd()
file_path = os.path.join(cwd, "song_dataset.csv")
training_path = os.path.join(cwd, "training")
if not os.path.exists(training_path):
    os.makedirs(training_path)
json_path = os.path.join(training_path, "json")
if not os.path.exists(json_path):
    os.makedirs(json_path)
static_url_path = os.path.join(cwd, "static")

era = [1950, 1960, 1970, 1980, 1990, 2000, 2010]