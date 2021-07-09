# adds/updates movies' and actors' ids
import sys
import pathlib
import json

# holds all the data
data = []
# holds only the actors 
all_actors = []
# holds each actor's movie references
connections = [] 

movie_id = 0

file = 'data/all_movies.json'
with open(file, 'r+') as f:    
  # create a new file
  file_action = "a+"
    
  # add a json object to the empty list 
  # this is the default layout of the actors.json file
  data.append({
    "actors": [],    
    "connections": []
  }) 
  
  movies = json.load(f) 

  all_actors = data[0]['actors']
  connections = data[0]['connections']

  for movie in movies:
    movie['id'] = 'm-' + str(movie_id)

    cast = movie['cast']
    for actor in cast:
      # only add the actor that is not in the all_actors list
      if actor['name'] not in all_actors:
        all_actors.append(actor['name'])

        # create a connection object for the new actors only
        connections.append({
          "name": actor['name'],
          "id": actor['id'],
          "in": [movie['id']]
        })
      else:
        # get the reference of the movie's id from the existing actor
        # to include it in the connections object
        actor_id = all_actors.index(actor['name'])

        if movie['id'] not in connections[actor_id]['in']:
          connections[actor_id]['in'].append(movie['id'])

    # end of cast for loop

    movie_id += 1  
  # end of movies for loop

  #reset file position to the beginning
  f.seek(0)
  json.dump(movies, f, indent=2) 
  f.truncate()

  # create/dump all_actors into the actors.json file
  with open("data/actors.json", file_action, encoding='utf-8') as af:
    json.dump(data, af, ensure_ascii=True, indent=2)