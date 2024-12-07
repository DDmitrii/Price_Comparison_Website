from Data_Base0 import Book
from bookitem import BookItem
#from livelib import getLivelib

import csv

# class BookItem(scrapy.Item):
#     name = scrapy.Field()
#     discountedprice = scrapy.Field()
#     fullprice = scrapy.Field()
#     link = scrapy.Field()
#     image = scrapy.Field()
#     author = scrapy.Field()
#     websitename = scrapy.Field()


class DBPipeline:
  def set_db(db):
    DBPipeline.db = db
  def process_item(self, item : BookItem, spider):
    # livelibbook = getLivelib(item['name'])
    DBPipeline.db.add_book(
      Book(name = item['name'],
            price = item['discountedprice'],
            # rating = livelibbook.rating
            book_link = item['link'],
            image_link = item['image'],
            website_name = item['websitename']
            ),
            # genres= livelibbook.tags,
            genres = ["Фантастика"],
            authors = item['author']
    )
    return item

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