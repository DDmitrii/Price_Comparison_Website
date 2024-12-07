import scrapy
#from Data_Base import db
#from Data_Base import Book
from livelib import getLivelib

import csv

class BookItem(scrapy.Item):
    name = scrapy.Field()
    discountedprice = scrapy.Field()
    fullprice = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()
    author = scrapy.Field()
    websitename = scrapy.Field()

'''
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
'''
class CSVPipeline:
  def open_spider(self, spider):
    self.file = open('BooksCSV.csv', 'w', newline='', encoding='utf-8')
    self.writer = csv.writer(self.file, delimiter = ';')
    self.writer.writerow(['Название', 'Автор','Цена со скидкой', 'Цена без скидки', 'Ссылка', 'Картинка'])    

  def close_spider(self, spider):
    self.file.close()

  def process_item(self, item, spider):
    self.writer.writerow([item['name'], item['author'], item['discountedprice'], item['fullprice'], item['link'], item['image']])
    return item