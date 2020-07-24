# create a json data file for the d3 force layout graph
import pathlib
import json

# hold the data for nodes and links
nodes = [] # holds the movies and the actors 
links = []

movies_file = 'data/all_movies.json'
actors_file = 'data/actors.json'

# for keeping track of actors nodes
all_actors = json.load(open(actors_file))[0]['actors']

# load in the all_movies.json
with open(movies_file) as m_f:
  movies = json.load(m_f)

  for movie in movies:
    # create movie "nodes" 
    movie_node = {
      "type": "movie",
      "name": movie['name'],
      "id": movie['id'],
      "year": movie['year'],
      "genre": movie['genre']      
    }
    nodes.append(movie_node)
    
    # source index for the links (the movie node is the source)
    movie_index = len(nodes)-1    

    # create actor "nodes"
    # get the actors array
    actors = movie['cast']
    for actor in actors:
      # only create a new node if the actor is in the all_actors array
      if actor['name'] in all_actors:
        # create a new entry to add to the main nodes array
        actor_node = {
          "type": "actor",
          "name": actor['name'],
          "id":  actor['id']
        }
        nodes.append(actor_node)
        # to keep track of which actor became a node, 
        # remove that actor from all_actors array
        all_actors.remove(actor['name'])

        # target index for the links (the actor node is the target)
        actor_index = len(nodes) - 1
      else:
        # there is an existing node for the current actor
        # therefore find its index position in the nodes array
        # to to use it for the link
        for entry in nodes:
          if (actor['name'] == entry['name']):
            actor_index = nodes.index(entry)
           
      # create links
      link = {
        "source": movie_index,
        "target": actor_index
      }
      links.append(link)   

with open('data/force_data.json', 'w') as f:
  json.dump({
    "nodes": nodes,
    "links": links
  }, f, indent = 2) 