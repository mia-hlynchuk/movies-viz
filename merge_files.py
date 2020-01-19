# merge all the movies_list_* files into one
# by looping through the json files 
# and appending each movie to a new array
# and then writing the new array into the new json file

import glob
import json

# will store all the movies
all_data = []

# get all the files starting with 'movies_list_' in their name 
for file in glob.glob('data/movies_list_*[0-9]*.json'):
  print(file)

  # load the data from the json file
  with open (file) as json_file:
    movies_data = json.load(json_file)

    # add each movie into the all_data array
    for movie in movies_data:
      all_data.append(movie)

with open('data/all_movies.json', 'w') as f:
  json.dump(all_data, f, indent=2)
