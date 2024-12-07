from .data_base.Data_Base import Book
from .bookitem import BookItem
from .livelib import getLivelib

import csv

class DBPipeline:
  def set_db(db):
    DBPipeline.db = db
  def process_item(self, item : BookItem, spider):
    tags = ""
    livelibbook = getLivelib(item['name'])
    if livelibbook is not None:
      tags = livelibbook.tags
    DBPipeline.db.add_book(
      Book(name = item['name'],
            price = item['discountedprice'],
            # rating = livelibbook.rating
            link = item['link'],
            image_link = item['image'],
            website_name = item['websitename']
            ),
            genres= tags,
            authors = item['author'].split(',')
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