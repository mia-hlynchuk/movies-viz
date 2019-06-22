#movies_list_spider.py

import scrapy

YEAR = '2000'
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
  def __init__(self, year=None, *args, **kwargs):
    super(MovieSpider, self).__init__(*args, **kwargs)
    YEAR = str(year)
    self.start_urls = [URL + YEAR]

  # deal with the http response
  def parse(self, response):
    print(response.url)

    movies = response.xpath('//*[@id="mw-content-text"]/div/table[contains(@class, "wikitable")]/tbody/tr[position()>1]')

    for movie in movies:
      # exclude documentary/concert genre
      _genre = movie.xpath('td[4]/descendant-or-self::text()').extract()
      genre = ''.join(_genre).split(', ')

      if len(genre)==0 or not (any(x in ['Documentary','Nature documentary','Concert'] for x in genre)):
        #name_selector = movie.xpath('td[1]/i/a/text()').extract()[0]
        # in 2012 and 2013 tables some movie names and cast are more nested 
        name = movie.xpath('td[1]/i/descendant-or-self::text()').extract()[0] 
        cast = movie.xpath('td[3]/descendant-or-self::text()').extract()
      
        # need to do this because the cast returns ',' as an array item
        updated_cast = ''.join(cast).split(', ')
        
        # seperate each actor into its own object
        castArray = []
        for actor in updated_cast:
          castArray.append({'name': actor }) # need to include id
        
        yield MovieItem(
          name = name,
          cast = castArray,
          genre = genre,
          year = YEAR
        )   