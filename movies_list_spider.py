#movies_list_spider.py

import scrapy

YEAR = '2000'
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
  name = 'movies_list'
  allowed_domains = ['en.wikipedia.org']
  start_urls = [URL]

  # deal with the http response
  def parse(self, response):
    print(response.url)

    movies = response.xpath('//*[@id="mw-content-text"]/div/table[contains(@class, "wikitable")]/tbody/tr[position()>1]')

    for movie in movies:
      name_selector = movie.xpath('td[1]/i/a/text()').extract()[0]
      cast_selector = movie.xpath('td[3]/a/text()').extract()
      # seperate each actor into its own object
      cast = []
      for actor in cast_selector:
        cast.append({'name': actor }) # need to include id

      genre_selector = movie.xpath('td[4]/descendant-or-self::text()').extract()

      yield MovieItem(
        name = name_selector,
        cast = cast,
        genre = genre_selector,
        year = YEAR
      )   