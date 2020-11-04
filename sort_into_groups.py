# Adds 'group' property to two data files (all_movies.json and actors.json)
# in all_movies.json each movie object will have the 'group' property
# in actors.json in 'connections' each actor object will have the 'group' property
import json
import sys

sys.setrecursionlimit(4000)

movies_file = 'data/all_movies.json'
actors_file = 'data/actors.json'

actors_data = json.load(open(actors_file))[0]
# holds references to the movies that the actors were in
a_connections = actors_data['connections'] 

# return the index position for either movie or actor
def get_index(id_string):
  return int(id_string.split('-')[1])
# end of get_index()

# for each cast member of the movie, 
# assign it and it's movies a 'group' property
def add_groups(cast, groupNum, main_movie_index): 
  for actor in cast:  
    # get the actor's index, so that we can look up the actor's movies that they were in
    actor_index = get_index(actor['id'])    
    current_actor = a_connections[actor_index]

    if 'group' not in current_actor:
      current_actor['group'] = groupNum

      for movie_id in current_actor['in']:
        movie_index = get_index(movie_id)

        # the first movie reference will always be the same as the main/current movie  
        #  so we don't need to loop through it      
        if movie_index != main_movie_index:
          # go back to the all_movies list to get the movie with the specified index
          if 'group' not in all_movies[movie_index]:
            all_movies[movie_index]['group'] = groupNum
            add_groups(all_movies[movie_index]['cast'], groupNum, movie_index)
# end of loop_cast()


with open(movies_file, 'r+') as m_f:
  all_movies = json.load(m_f)

  current_group = 1

  for current_movie in all_movies:
    index = get_index(current_movie['id'])
 
    if 'group' not in current_movie:
      current_movie['group'] = current_group
      add_groups(current_movie['cast'], current_group, index)
      current_group += 1
      
  m_f.seek(0)
  json.dump(all_movies, m_f, indent=2)
  m_f.truncate()


  # update the actors.json 'connections" with groups
  with open('data/actors.json', 'w', encoding='utf-8') as af:
    af.seek(0)
    json.dump(actors_data, af, ensure_ascii=True, indent=2)