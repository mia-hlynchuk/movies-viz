# based on the year selected, edit/sort the movies' and the actors' ids
# in the command line type: loading_json_data.py arg1 arg2 
#   argv1 - (year), the file ending in that year that you want to edit
#   argv2 - (movie_id), the starting id that will be used to iterate throught movies ids
import sys
import pathlib
import json

# holds all the data
data = []
# holds the current data from the actors.json file
actors_file = []
# holds only the actors 
all_actors = []
# holds each actor's movie refrences
connections = [] 

# the starting out movie id will depend on the parameter we give in the terminal
movie_id = int(sys.argv[2])
file_to_load = ''

def file_year(year):
  # the file we want to load
  file = 'data/movies_list_' + year +'.json'
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
  actors_file = pathlib.Path("data/actors.json")
  if actors_file.exists():
    # load the data from the existing file into the data list
    json_file = open('data/actors.json')
    data = json.load(json_file)
   
    json_file.close()
    file_action = "r+"
  else:
    # create a new file
    file_action = "a+"
    
    # add a json object to the empty list 
    # this is the default layout of the actors.json file
    data.append({
      "actors": [],    
      "connections": []
    }) 
  
  # load the year file that we want to edit
  movies = json.load(f) 

  all_actors = data[0]['actors']
  connections = data[0]['connections']

  for movie in movies:
    movie['id'] = 'm-' + str(movie_id)

    cast = movie['cast']
    for actor in cast:
      # only add the actor that is not in the all_actors list
      if actor['name'] not in all_actors:
        all_actors.append(actor['name'])

        # create a connection object for the new actors only
        connections.append({
          "name": actor['name'],
          "in": [movie['id']]
        })
      else:
        # get the refrence of the movie id from the existing actor
        # to include it in the connections object
        a_id = all_actors.index(actor['name'])

        # only add it once, just in case we need to rerun the year
        if movie['id'] not in connections[a_id]['in']:
          connections[a_id]['in'].append(movie['id'])
         
      # find the index of the actor and make it into its id
      actor['id'] = 'a-' + str(all_actors.index(actor['name']))

    # end of cast for loop

    movie_id += 1  
  # end of movies for loop

  # in the command line, when we call the next json file
  # this is the new value that we need to include for arg2
  print( 'the next movie_id: ' + str(movie_id) ) 

  #reset file position to the beginning
  f.seek(0)
  json.dump(movies, f, indent=2) 
  f.truncate()

  # create/dump all_actors into the actors.json file
  # will store all the actors from all the years files
  with open("data/actors.json", file_action, encoding='utf-8') as af:
    json.dump(data, af, ensure_ascii=True, indent=2)