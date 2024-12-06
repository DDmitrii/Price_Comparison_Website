import scrapy
from Data_Base import db
from Data_Base import Book
from livelib import getLivelib

class BookItem(scrapy.Item):
    name = scrapy.Field()
    discountedprice = scrapy.Field()
    fullprice = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()
    author = scrapy.Field()
    websitename = scrapy.Field()

class ParsePipeline:
  def process_item(self, item : BookItem, spider):
    livelibbook = getLivelib(item['name'])
    db.add_book(
      Book(name = item['name'],
            price = item['discountedprice'],
            rating = livelibbook.rating),
            genres= livelibbook.tags,
            authors = item['author']
    )
    return item