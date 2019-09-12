#movies_list_v2_spider.py
# different layout of the wikitables 2014 and up

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
  name = 'movies_list_v2'
  allowed_domains = ['en.wikipedia.org']
 
  # passing an argument to the spider
  # in the terminal type '-a year=2000'
  def __init__(self, year, *args, **kwargs):
    super(MovieSpider, self).__init__(*args, **kwargs)
    self.year = year    
    self.start_urls = [URL + self.year]


  # deal with the http response
  def parse(self, response):
    movies_selector = response.xpath('//*[@id="mw-content-text"]/div/table[contains(@class, "wikitable")]/tbody/tr[position()>1]')
    tr_i = 0
    for movie in movies_selector: 
      tr_i += 1 
      #print(tr_i)

      # select <td> elements with rowspan attribute only
      td_rowspan = movie.xpath('td[@rowspan]')

      # a few <td> elements have align or style attribute instead of rowspan
      td_align = movie.xpath('td[1][@align]')
      td_style = movie.xpath('td[1][@style]')      
        
      # the default index for the xpath for the <td> elements
      td_name_index = '1' 
      td_cast_index = '3'
      td_genre_index = '4'

      if len(td_rowspan) == 2 or (self.year=='2015' and tr_i==114):
        td_name_index = '3'
        td_cast_index = '5'
        td_genre_index = '6'
      elif len(td_rowspan) == 1 or td_align or td_style or (self.year=='2015' and (tr_i==113 or tr_i==120 or tr_i==126 or tr_i==139)):
        td_name_index = '2'
        td_cast_index = '4'
        td_genre_index = '5'
       

      cast = movie.xpath('td['+ td_cast_index +']/descendant-or-self::text()').extract()
      genre = movie.xpath('td['+ td_genre_index +']/descendant-or-self::text()').extract()

      # remove the empty quotes from the cast and the genre lists
      for a_list in [cast, genre]:
        while '\n' in a_list:
          a_list.remove('\n')
        while ' ' in a_list:
          a_list.remove(' ')
        # for 2017 and up
        while ', ' in a_list:
          a_list.remove(', ')
      
      # exclude documentary and concert related genres
      if len(genre)==0 or not (any(x in ['Documentary','Nature documentary','Concert','Political documentary','Biopic Documentary'] for x in genre)):
        name = movie.xpath('td['+ td_name_index +']/descendant-or-self::text()').extract()[0]

        # join the cast list into a string
        cast_string = ','.join(cast).strip()
        
        # fix the ', Jr.,' format
        cast_string = cast_string.replace(', Jr.', ' Jr.')

        # for 2017 and up the cast column changed to include the director and screenplay people, 
        # therefore we need to remove them before storing the actors' names
        if int(self.year) >= 2017:
          # seperate the genre string into a list
          updated_genre = genre[0].strip().split(', ')

          # get the beginning of the string till the end of ';' 
          to_remove = re.findall(r"^.*\(.*?\)\;", cast_string)
            
          if to_remove:           
            # split the string back to a list
            updated_cast = cast_string.replace(to_remove[0], '').split(',')
        else:
          updated_cast = cast_string.split(',')
          updated_genre = genre
      
        # seperate each actor into its own object
        castArray = []
        for actor in updated_cast:
          # exclude the empty string entries
          if actor.strip():
            # use the actor's stage name if there is one instead
            if re.findall(r'["\'](.*?)["\']', actor):                
              actor = re.findall(r'["\'](.*?)["\']', actor)[0]
            castArray.append({'name': actor.strip() }) # need to include id
        
        # capitalize the genre entries
        genreArray = []
        for g in updated_genre:
          genreArray.append(g.title())
      
        yield MovieItem(
          name = name,
          cast = castArray,
          genre = genreArray,
          year = self.year
        )