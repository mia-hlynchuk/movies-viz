#movies_list_v2_spider.py
# different layout of the wikitables after the 2013 year

import scrapy

YEAR = '2014'
URL = 'http://en.wikipedia.org/wiki/List_of_American_films_of_'+ YEAR

# define the data that will be scraped
class MovieItem(scrapy.Item):
  name = scrapy.Field()
  cast = scrapy.Field()
  genre = scrapy.Field()
  year = scrapy.Field()

# our spider, scrapes the movie's name, cast, and genre
class MovieSpider(scrapy.Spider):
  # name of the spider to call in the terminal
  name = 'movies_list_v2'
  allowed_domains = ['en.wikipedia.org']
  start_urls = [URL]

  # deal with the http response
  def parse(self, response):
    movies_selector = response.xpath('//*[@id="mw-content-text"]/div/table[contains(@class, "wikitable")]/tbody/tr[position()>1]')
    for movie in movies_selector:  
      # select <td> elements with rowspan attribute only
      td_rowspan = movie.xpath('td[@rowspan]')
        
      # the default index for the xpath for the <td> elements
      td_name_index = '1' 
      td_cast_index = '3'
      td_genre_index = '4'

      if len(td_rowspan) == 2:
        td_name_index = '3'
        td_cast_index = '5'
        td_genre_index = '6'
      elif len(td_rowspan) == 1:
        td_name_index = '2'
        td_cast_index = '4'
        td_genre_index = '5'
 
      name = movie.xpath('td['+ td_name_index +']/descendant-or-self::text()').extract()[0]
      cast_selector = movie.xpath('td['+ td_cast_index +']/descendant-or-self::text()').extract()
      # seperate each actor into its own object
      cast = []
      for actor in cast_selector:
        cast.append({'name': actor }) # need to include id
      
      genre = movie.xpath('td['+ td_genre_index +']/descendant-or-self::text()').extract()

      yield MovieItem(
        name = name,
        cast = cast,
        genre = genre,
        year = YEAR
      )   