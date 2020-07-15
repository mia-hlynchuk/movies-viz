#movies_list_spider.py

import scrapy
import re

URL = 'https://en.wikipedia.org/wiki/List_of_American_films_of_2019'

# define the data that will be scraped
class MovieItem(scrapy.Item):
  name = scrapy.Field()
  cast = scrapy.Field()
  genre = scrapy.Field()
  year = scrapy.Field()

# our spider, scrapes the movie's name, cast, and genre
class MovieSpider(scrapy.Spider):
  # name of the spider to call in the terminal
  name = 'movies_list_2019'
  allowed_domains = ['en.wikipedia.org']
  start_urls = [URL]

  # deal with the http response
  def parse(self, response):
    movies = response.xpath('//*[@id="mw-content-text"]/div/table[contains(@class, "wikitable")]/tbody/tr[position()>1]')  
    
    for movie in movies:
      td_rowspan = movie.xpath('td[@rowspan]')
      td_style = movie.xpath('td[1][@style]')

      # the default index for the xpath for the <td> elements
      td_name_index = '1' 
      td_cast_index = '3'
      td_genre_index = '4'

      if td_rowspan or td_style:
        td_name_index = '2'
        td_cast_index = '4'
        td_genre_index = '5'

      cast = movie.xpath('td['+ td_cast_index +']/descendant-or-self::text()').extract()
      genre = movie.xpath('td['+ td_genre_index +']/text()').extract()[0]

      # separate the genre string into a list
      genre = genre.replace(r'\\n', '').split(', ')

      if not 'Documentary' in genre:
        name = movie.xpath('td['+ td_name_index +']/descendant-or-self::text()').extract()[0]
        #print(name)      

        # join the cast list into a string
        cast_string = ','.join(cast).strip()

        # get the beginning of the string till the end of ';'  
        to_remove = re.findall(r"^.*\(.*?\)\;", cast_string)
        if to_remove:           
          # split the string back to a list
          updated_cast = cast_string.replace(to_remove[0], '').split(',')
        else:
          updated_cast = cast
          
        
        # remove the empty spaces in the updated cast list
        while "\n" in updated_cast:
          updated_cast.remove("\n")
        while " " in updated_cast:
          updated_cast.remove(" ")
        while "" in updated_cast:
          updated_cast.remove("")
        
        # separate each actor into its own object
        castArray = []
        for actor in updated_cast:
          castArray.append({'name': actor.strip() }) # need to include id
        
        yield MovieItem(
          name = name,
          cast = castArray,
          genre = genre,
          year = 2019
        )