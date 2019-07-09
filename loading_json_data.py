# based on the year selected, edit/sort the movies' and the actors' ids
# in the command line type: loading_json_data.py 2002
import sys
import json

# store all the actors from every movie in one place
all_actors = []
# give each movie and actor a unique id
movie_id = 0
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
  # load the year file that we want to edit
  movies = json.load(f) 
  for movie in movies:
    movie['id'] = 'm-' + str(movie_id)

    cast = movie['cast']
    for actor in cast:
      # only add the actor that  is not in the all_actors list
      if not (actor['name'] in all_actors):
        all_actors.append(actor['name'])
        
      # find the index of that actor and make it into its id
      actor['id'] = 'a-' + str(all_actors.index(actor['name']))
    # end of actors for loop

    movie_id += 1  
  # end of movies for loop

  print( 'last movie id: ' + str(movie_id) ) 
  print( 'last actor id: ' + str(len(all_actors)) )

  #reset file position to the beginning
  f.seek(0)
  json.dump(movies, f, indent=2) 
  f.truncate()

  # create/dump all_actors into a json file
  # will store all the actors from all the years files
  with open("actors.json","a+") as af:
    json.dump(all_actors, af, indent=2)