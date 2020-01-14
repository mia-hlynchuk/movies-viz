# create a json data file for the d3 force layout graph
import pathlib
import json

# hold the data for nodes and links
nodes = [] # holds the movies and the actors 
links = []

movies_file = 'data/all_movies.json'
actors_file = 'data/actors.json'

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

# load actors.json
with open(actors_file) as a_f:
  actors = json.load(a_f)[0]['connections']
  
  # create actor "nodes" 
  a_index = 0 # used for assigning the id for the actors
  for actor in actors:
    actor_node = {
      "type": "actor",
      "name": actor['name'],
      "id": "a-" + str(a_index)
    }
    nodes.append(actor_node)

    # create "links" objects
    connections = actor['in']
    for link in connections:
      # extract the movie's id number
      m_id = link.split("-")[1]
      link = {
        # the source is the last actor that was added to the nodes array  
        "source": len(nodes) - 1,
        # the target is the movie
        "target": m_id
      }
      links.append(link)
    
    a_index += 1

with open('data/force_data.json', 'w') as f:
  json.dump({
    "nodes": nodes,
    "links": links
  }, f, indent = 2)
 