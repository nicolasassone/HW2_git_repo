# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    #the url we start on. In my example, we use the link to game of thrones
    start_urls = ['https://www.imdb.com/title/tt0944947/']

    #First parse method
    def parse(self, response):
        sitelink=response.urljoin("fullcredits")
        yield scrapy.Request(sitelink, callback=self.parse_full_credits)

    def parse_full_credits(self, response):

        #scrapes the path to each picture of the actors of the cast on the fullcredits page
        actor_paths=[a.attrib['href'] for a in response.css('td.primary_photo a')]

        #creates a list of links to each actor in the cast using the list of paths above
        actor_links = ['https://www.imdb.com' + path for path in actor_paths]

        #for every url to each actor in the above list, it calls the next parse method
        for url in actor_links:

            #for each actor, calls the parse_actor_page method
            yield scrapy.Request(url, callback = self.parse_actor_page)

    def parse_actor_page(self, response):

        #for loop which iterates once to navigate to the header section
        #containing the name of the actor, and then uses string operations
        #to pull out the actor's precise full name
        for header in response.css('h1.header'):
            name = header.css("span.itemprop").get()
            name=((name.split('>'))[1].split('<'))[0]

        #for loop which runs through all the different movies
        #of this fixed actor, and then uses string operations 
        #to pull out the exact name of the movie the actor was in
        for movie in response.css("div.filmo-row"):
            title=movie.css("a::text")
            title = str(title[0])
            title = (title.split("'"))[3]

            #creates a .csv spreadsheet with two columns containing an actor
            #and the movie they were in. This is nexted in the above for loop, 
            #and so it runs through every movie the actor was in
            yield {"actor" : name, "movie_or_TV_name" : title}
