# Movies Visualization

## Getting the data

#### From Wikipedia
Using [Scrapy](https://scrapy.org/) to scrape the movies data from [Wikipedia](https://en.wikipedia.org/wiki/List_of_American_films_of_2000).

Get the movies from the specified year. There are 3 spiders because some of the pages have a different table layout.
	`movie_list` scrapes 2000 to 2013
	`movies_list_v2` scrapes 2014 to 2018
	`movies_list_2019` scrapes 2019

In the terminal:
	`scrapy crawl {spider name} -a year={year} -o data/movies_list_{year}.json`

#### From The Movie Database
Using [The Movie Database](https://www.themoviedb.org/) to get more information about each movie.

In the terminal:
	`python get_more_info.py {year}`

## Sorting the Data
Assign ids to the movies and actors. There are two ways. Both options will produce `actors.json` It will store only the actors and the references to the movies they were in.

### Option 1
First add ids directly to the movies_list_ files. This is good if you want to use the files individually. 

In the terminal:
	`python loading_json_data.py {year} {movie id}` 

For the {year} specified assign ids to the movies and actors. The starting out {movie id} will be the one specified in the terminal. 

Then combine all the movies_list_ files into `all_movies.json` 

In the terminal: 
	`python merge_files.py`

### Option 2
First combine all the movies_list_ files into `all_movies.json` 

In the terminal:
	`python merge_files.py`

Then add the ids, but they will be added to the `all_movies.json` file only. The movies_list_ files will not be affected.

In the terminal:
	`python add_ids.py`
	

## Formatting the data
Create `force_data.json` for the D3 Force Layout graph

In the Terminal:
	`python sort_into_force_data.py`
