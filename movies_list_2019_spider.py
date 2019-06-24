#movies_list_spider.py

import scrapy
import re

URL = 'https://en.wikipedia.org/wiki/2019_in_film'

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
    movies = response.xpath('//*[@id="mw-content-text"]/div/table[contains(@class, "wikitable")][position()>5]/tbody/tr[position()>1]')
    
    for movie in movies:
      # select <td> elements with rowspan attribute only
      td_rowspan = movie.xpath('td[@rowspan]')

      # a few <td> elements have align or style attribute instead of rowspan
      td_align = movie.xpath('td[1][@align]')
      td_style = movie.xpath('td[1][@style]')
        
      # the default index for the xpath for the <td> elements
      td_name_index = '1' 
      td_cast_index = '3'
      td_genre_index = '4'

      if len(td_rowspan) == 2:
        td_name_index = '3'
        td_cast_index = '5'
        td_genre_index = '6'
      elif len(td_rowspan) == 1 or td_align or td_style:
        td_name_index = '2'
        td_cast_index = '4'
        td_genre_index = '5'
    
      cast = movie.xpath('td['+ td_cast_index +']/descendant-or-self::text()').extract()
      genre = movie.xpath('td['+ td_genre_index +']/text()').extract()
  
      if len(genre)==0 or not (any(x in ['Documentary','Nature documentary','Concert'] for x in genre)):
        name = movie.xpath('td['+ td_name_index +']/i/a/text()').extract()[0]
        
        # seperate the genre string into a list
        updated_genre = genre[0].replace(r'\\n', '').split(',')

        # join the cast list into a string
        cast_string = ','.join(cast)
        # get the beginning of the string till the end of ';'  
        to_remove = re.findall(r"^.*\(.*?\)\;\s,", cast_string)
        if to_remove:           
          # split the string back to a list
          updated_cast = cast_string.replace(to_remove[0], '').split(',')
        else:
          updated_cast = cast
          updated_genre = genre

        # remove the empty spaces in the updated cast list
        while "\n" in updated_cast:
          updated_cast.remove("\n")
        while " " in updated_cast:
          updated_cast.remove(" ")
        while "" in updated_cast:
          updated_cast.remove("")

        # seperate each actor into its own object
        castArray = []
        for actor in updated_cast:
          castArray.append({'name': actor }) # need to include id

        yield MovieItem(
          name = name,
          cast = castArray,
          genre = updated_genre,
          year = 2019
        )