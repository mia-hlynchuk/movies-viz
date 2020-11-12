 # !! You can only run this file once !!
 # organize the order of the movies in all_movies.json file
 # instead of being shown by year, they are sorted by actor's reference

import json

movies_file = 'data/all_movies.json'
actors_file = 'data/actors.json'

with open(movies_file, 'r+') as m_file:
  all_movies = json.load(m_file)

  updated_movies = []
  movies_index_tracker = []

  with open(actors_file, 'r') as a_file:  
    all_actors = json.load(a_file)
    
    for actor in all_actors['connections']:
      movies_references = actor['in']
  
      for ref in movies_references:
        # get the index number
        m_index = int(ref.split('-')[1])
        
        # check if we already added the index number
        if m_index not in movies_index_tracker:
          movies_index_tracker.append(m_index)
          updated_movies.append(all_movies[m_index])  
  m_file.seek(0)
  json.dump(updated_movies, m_file, ensure_ascii=True, indent=2)
  m_file.close()