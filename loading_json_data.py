# based on the year selected, edit/sort the movies' and the actors' ids
# in the command line type: loading_json_data.py arg1 arg2 
#   argv1 - (year), the file ending in that year that you want to edit
#   argv2 - (movie_id), the starting id that will be used to iterate throught movies ids
import sys
import pathlib
import json

# store all the actors from every movie in one place
all_actors = []
# the starting out movie id will depend on the parameter we give in the terminal
movie_id = int(sys.argv[2])
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
  # check to see if the actors.json file exists
  actors_file = pathlib.Path("actors.json")
  if actors_file.exists():
    json_file = open('actors.json')
    # load the actors from the existing actors file into the all_actors list
    all_actors = json.load(json_file)
    json_file.close()
    file_action = "r+"
  else:
    file_action = "a+"
  
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

  #  in the command line, when we call the next json file
  # this is the new value that we need to include for arg2
  print( 'the next movie_id: ' + str(movie_id) ) 

  #reset file position to the beginning
  f.seek(0)
  json.dump(movies, f, indent=2) 
  f.truncate()

  # create/dump all_actors into the actors.json file
  # will store all the actors from all the years files
  with open("actors.json", file_action) as af:
    json.dump(all_actors, af, indent=2)