from scrapy.crawler import CrawlerProcess
from mif import MIFSpider
from chitaigorod import CGSpider
from livelib import getTags
from labirint import LBSpider


process = CrawlerProcess()
process.crawl(LBSpider)
process.start()

import requests 

#query = 'Амогус'
#book = getTags(query)
#print("Name: ", book.name)
#print("Author: ", book.author)
#print("Image: ", book.image)
#print("Livelib: ", book.liveliblink)
#print("Tags: ", book.tags)
#print("Rating: ", book.rating)
#response = requests.get("https://livelib.ru/find/works/"+ query.replace(" ", "+")) 

#with open("output.html", "w") as file:
    #file.write(response.text)