# based on the year selected, find more cast memebers and get the genre of the movie
# using 'The Movie DB' API and 'tmdbsimple' library
# in the command line type: get_more_info.py {year}
import config
import sys
import json
import re
import tmdbsimple as tmdb
import time

# API key
tmdb.API_KEY = config.api_key

current_year = sys.argv[1]

file_to_load = ''

def file_year(year):
  # the file we want to load
  file = 'movies_list_' + year +'.json'
  print(file)
  return file

# get the parameter from the command line
if __name__ == "__main__":
  file_to_load = file_year(sys.argv[1])


with open(file_to_load, 'r+') as f:
  # load the json year file that we want to add more actors to
  f_movies = json.load(f)

  # keeps track of the url request limit 
  request_count = 0

  # movies that the TMDB can't find, because its not under the correct year
  # need to delete and edit the movies into the correct file manually
  issues_movies = []

  for f_movie in f_movies:
    if request_count < 39:
      # this would be our search query
      title  = f_movie['name'] 
      
      # 1st url request
      search = tmdb.Search()
      search.movie(query=title, year=current_year) #primary_release_year
      print("# of results: " + str(len(search.results))) 

      file_cast = f_movie['cast']
      
      if len(search.results) == 0:
        #print("ISSUE:" + title)
        issues_movies.append(title)
      else:
        print("-------------")
        # the movie's id from the movie database
        m_id = search.results[0]['id']
      
        print(m_id) 
        print(title.upper())

        tmdb_movie = tmdb.Movies(m_id)
        # 2nd url request: get the cast's names
        db_cast = tmdb_movie.credits()['cast']
        # 3rd url request: get the genres
        db_genres = tmdb_movie.info()['genres']
      
        # store the file's cast members in an array
        file_cast_array = []
        for f_actor in file_cast:
          file_cast_array.append(f_actor['name'])
        # end file_cast for loop

        # check the db_cast names against the existing cast
        # if they are not included, add them
        for db_actor in db_cast:
          name = db_actor['name']
          if not (name in file_cast_array):
            f_movie['cast'].append({"name":name})  
        # end db_cast for loop      

        # only add genres that are missing 
        for db_g in db_genres:
          #print(db_g['name'])
          if not (db_g['name'] in f_movie['genre']):
            f_movie['genre'].append(db_g['name'])
        # end db_genres for loop

      # because we are making 3 url requests in each iteration
      # we need to increment by 3
      request_count += 3 
    else:
      # when the request_count reaches its limit
      # pause the system for 15 seconds 
      # and reset the request_count
      print("SLEEP---------")
      time.sleep(15)
      request_count = 0      
  # end f_movies for loop

  print(issues_movies)

  #reset file position to the beginning
  f.seek(0)
  json.dump(f_movies, f, indent=2) 
  f.truncate()    