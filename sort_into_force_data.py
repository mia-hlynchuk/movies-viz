# create a json data file for the d3 force layout graph
import pathlib
import json

# holds the data for nodes and links
nodes = [] # holds the movies and the actors 
links = []

movies_file = 'data/filtered_movies.json'
actors_file = 'data/actors.json'

actors_data = json.load(open(actors_file))

all_actors_id = actors_data['actors']
# to keep track of which actor became a node
actors_id_tracker = []


# load in the all_movies.json
with open(movies_file) as m_f:
  movies = json.load(m_f)

  for movie in movies:
    if(movie['show'] == True ):
      group_id = movie['group']
      
      # create movie "nodes" 
      movie_node = {
        "type": "movie",
        "name": movie['name'],
        "id": movie['id'],
        "year": movie['year'],
        "genre": movie['genre'],
        "group": group_id
      }
      nodes.append(movie_node)
      
      # source index for the links (the movie node is the source)
      node_movie_index = len(nodes)-1    

      # create actor "nodes"
      # get the actors array
      cast = movie['cast']
      for actor in cast:
        # make sure that the actor is in the filtered list
        if actor['id'] in all_actors_id:
          # check that the actor is only there once
          # we don't want any repeats
          if (actor['id'] in actors_id_tracker):
            # There is an existing node for the current actor,
            # therefore find its index position in the nodes array
            # to use it for the link entry
            for entry in nodes:
              if (actor['id'] == entry['id']):
                node_actor_index = nodes.index(entry)     
          else: # for a new node only     
            # create a new entry to add to the main nodes array
            # if its not in the actors_id_tracker, then it means that the node has not been created yet
            actor_node = {
              "type": "actor",
              "name": actor['name'],
              "id":  actor['id'],
              "group": group_id
            }    
            nodes.append(actor_node)
            
            actors_id_tracker.append(actor['id'])

            # target index for the links (the actor node is the target)
            node_actor_index = len(nodes) - 1
        
          # create links
          link = {
            "source": node_movie_index,
            "target": node_actor_index,
            "value":  group_id
          }
          #print(link)
          links.append(link)   
        # end of for actor in cast:

with open('data/force_data.json', 'w') as f:
  json.dump({
    "nodes": nodes,
    "links": links
  }, f, indent = 2) 
