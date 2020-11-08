# create a json data file for the d3 force layout graph
import pathlib
import json

# hold the data for nodes and links
nodes = [] # holds the movies and the actors 
links = []

movies_file = 'data/all_movies.json'
actors_file = 'data/actors.json'

print(actors_file)

actors_data = json.load(open(actors_file))
all_actors = actors_data['actors']
actors_connections = actors_data['connections']

# load in the all_movies.json
with open(movies_file) as m_f:
  movies = json.load(m_f)

  for movie in movies:
    group_id = movie['group']
      
    # create movie "nodes" 
    movie_node = {
      "type": "movie",
      "name": movie['name'],
      "id": movie['id'],
      "year": movie['year'],
      "genre": movie['genre'],
      "group": group_id,
      "show": True
    }
    nodes.append(movie_node)
      
    # source index for the links (the movie node is the source)
    node_movie_index = len(nodes)-1    

    # create actor "nodes"
    # get the actors array
    cast = movie['cast']
    for actor in cast:
      # reference to the index position in the actors.json file
      a_i = int(actor['id'].split('-')[1])

      # We can't have duplicated actor nodes. So by adding a symbol to the actor's name,
      # we can keep track of the actors that were appended to the 'nodes' array.
      if (actor['name']+'+') in all_actors:
        # There is an existing node for the current actor,
        # therefore find its index position in the nodes array
        # to use it for the link entry
        for entry in nodes:
          if (actor['name'] == entry['name']):
            node_actor_index = nodes.index(entry)     
      else: # for a new node only     
        # create a new entry to add to the main nodes array
        actor_node = {
          "type": "actor",
          "name": actor['name'],
          "id":  actor['id'],
          "group": group_id,
          "show": actors_connections[a_i]['show']
        }    
        nodes.append(actor_node)

        # to keep track of which actor became a node
        all_actors[a_i] += '+'

        # target index for the links (the actor node is the target)
        node_actor_index = len(nodes) - 1
        
      # create links
      link = {
        "source": node_movie_index,
        "target": node_actor_index,
        "value": group_id,
        "show": actors_connections[a_i]['show']
      }
      #print(link)
      links.append(link)   
      # end of for actor in cast:
  
with open('data/force_data.json', 'w') as f:
  json.dump({
    "nodes": nodes,
    "links": links
  }, f, indent = 2) 