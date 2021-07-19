# compare actors against each other to see what movies they have in common
# and save them to a new file 'filtered_movies.json'
import json

movies_file = 'data/all_movies.json'
actors_file = 'data/actors.json'
   

# holds the filtered out actors
filtered_connections = []
# for tracking actors that have been added to the filtered_connection list
actors_id_tracker = []

# holds the filtered out movies
filtered_movies = []
# for tracking movies that have been added to the filtered_movies list
movies_id_tracker = []

movies_in_common =2

all_movies_data = json.load(open(movies_file))
actors_data = json.load(open(actors_file))

def update_list(item_id, id_tracker, current_item, new_list):
  if item_id not in id_tracker:
    new_list.append(current_item)
    id_tracker.append(item_id)
  

connections = actors_data[0]['connections']
length = len(connections)
i = 0
# Actor A
for actor in connections:
  actor_a_id = actor['id']
  actor_a_in_movies = actor['in']
  actor_a_in_as_set = set(actor_a_in_movies)

  # Actor B
  # start comparing to the next actor in the list
  for j in range( i+1 , length-1): 
    actor_b_id = connections[j]['id']
    actor_b_in_movies = connections[j]['in']

    intersection = actor_a_in_as_set.intersection(actor_b_in_movies)
    intersection_as_list = list(intersection)

    # only extract the actors that have a specific # of movies in common
    if (len(intersection_as_list) == movies_in_common ): 
      #print(intersection_as_list)

      # Actor A
      update_list(actor_a_id, actors_id_tracker, actor, filtered_connections)
      # Actor B
      update_list(actor_b_id, actors_id_tracker, connections[j], filtered_connections)

      # change the 'show' value to True for all the movies that are in the intersection list
      for item in intersection_as_list:
        m_index = int(item.split('-')[1])
        all_movies_data[m_index]['show'] = True

        # only append movies that have True for 'show' value into the new filtered list
        update_list(item, movies_id_tracker, all_movies_data[m_index], filtered_movies )
        #update_list
      
    # end of intersection 
  i+=1
# end of looping through each actors' connections

with open('data/actors.json', 'w') as a_file:
  json.dump({
    "actors": actors_id_tracker,
    "connections": filtered_connections
  }, a_file, indent=2)


with open('data/filtered_movies.json', 'w', encoding='utf-8') as fm_file:
  json.dump(filtered_movies, fm_file, ensure_ascii=True, indent=2)