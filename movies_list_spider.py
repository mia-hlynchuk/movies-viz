#movies_list_spider.py

import scrapy
import re

URL = 'http://en.wikipedia.org/wiki/List_of_American_films_of_'

# define the data that will be scraped
class MovieItem(scrapy.Item):
  name = scrapy.Field()
  cast = scrapy.Field()
  genre = scrapy.Field()
  year = scrapy.Field()

# our spider, scrapes the movie's name, cast, and genre
class MovieSpider(scrapy.Spider):
  # name of the spider to call in the terminal
  name = 'movies_list'
  allowed_domains = ['en.wikipedia.org']

  # passing an argument to the spider  
  # in the terminal type '-a year=2000'
  def __init__(self, year, *args, **kwargs):
    super(MovieSpider, self).__init__(*args, **kwargs)
    self.year = year
    self.start_urls = [URL + year]

  # deal with the http response
  def parse(self, response):
    print(response.url)

    movies = response.xpath('//*[@id="mw-content-text"]/div/table[contains(@class, "wikitable")]/tbody/tr[position()>1]')

    for movie in movies:
      # exclude documentary/concert genre
      _genre = movie.xpath('td[4]/descendant-or-self::text()').extract() 
      genre = ''.join(_genre).title()
     
      # a few lists have different format for genre
      if (self.year=='2003' or self.year=='2007' or self.year=='2009' or self.year=='2010'):
        genre = genre.replace('/', ', ')

      genre = genre.strip().split(', ')

      if len(genre)==0 or not (any(x in ['Documentary','Nature documentary','Concert', 'Reality', 'Mockumentary', 'Rockumentary'] for x in genre)):
        # in 2012 and 2013 tables some movie names and cast are more nested 
        name = movie.xpath('td[1]/i/descendant-or-self::text()').extract()[0] 
        cast = movie.xpath('td[3]/descendant-or-self::text()').extract()
      
        # need to do this because the cast returns ',' as an array item
        # some cast are joined by 'and', we need to split them
        updated_cast = ''.join(cast).replace(' and ', ', ')
       
        # don't include movie entries that have descrition in the cast's cell
        if not re.search(r'(the\s)|(^A\s)|(\sof\s)|(\sby\s)', updated_cast):
          # fix the 'Jr.' and 'Sr.' format
          updated_cast = updated_cast.replace(', Jr.', ' Jr.')
          updated_cast = updated_cast.replace(', Sr.', ' Sr.')
          
          # remove words that are in () or 'introducing' or 'with'
          updated_cast = re.sub(r'(\((.*?)\))|(introducing\s)|(with\s)', '', updated_cast)
          
          # seperate each actor into its own object
          updated_cast = re.split('\, ', updated_cast)
          castArray = []
          for actor in updated_cast:
            # exclude the empty string entries
            if not actor == '':
              # use the actor's stage name if there is one instead
              if re.findall(r'["\'](.*?)["\']', actor):                
                actor = re.findall(r'["\'](.*?)["\']', actor)[0]

              castArray.append({'name': actor.strip() }) # need to include id
         
          yield MovieItem(
            name = name,
            cast = castArray,
            genre = genre,
            year = self.year
          )   