import scrapy
from Data_Base import db
from Data_Base import Book
from livelib import getTags

class BookItem(scrapy.Item):
    name = scrapy.Field()
    discountedprice = scrapy.Field()
    fullprice = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()
    author = scrapy.Field()

class ParsePipeline:
  def process_item(self, item : BookItem, spider):
    tags = getTags(item['name'])
    db.add_book(
      Book(name = item['name'],
            price = item['fullprice']),
            genres= tags,
            authors = item['author']
    )
    return item