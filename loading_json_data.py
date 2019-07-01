# based on the year selected, edit/sort the movies' and the actors' ids
# in the command line type: loading_data.py 2002
import sys
import json

# store all the actors from every movie in one place
all_actors = []
# give each movie and actor a unique id
movie_id = 0
actor_id = 0
file_to_load = ''

def file_year(year):
  # the file we want to load
  file = 'movies_list_' + year +'.json'
  print(file)
  return file

# get the parameter from the command line
if __name__ == "__main__":
  file_to_load = file_year(sys.argv[1])
  
print("FILE TO LOAD:")
print(file_to_load)
print("===================")
with open(file_to_load, 'r+') as f:
  movies = json.load(f)
   

  for movie in movies:
    movie['id'] = 'm-' + str(movie_id)

    m_name = movie['name']
    print('MOVIE:' + m_name)
    
    cast = movie['cast']
    for actor in cast:
      actor['id'] = 'a-' + str(actor_id)
      # add the actor to the main list of actors
      all_actors.append(actor)
      actor_id += 1
    # end of actors for loop

    movie_id += 1  
  # end of movies for loop

  print('last movie id: ' + str(movie_id)) 
  print('last actor id: ' + str(actor_id)) 

  #reset file position to the beginning
  f.seek(0)
  json.dump(movies, f) 
  f.truncate()
    