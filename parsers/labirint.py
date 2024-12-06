from parser import BookItem
import csv
import scrapy
from bs4 import BeautifulSoup

class LBPipeline:
  def open_spider(self, spider):
    self.file = open('LB.csv', 'w', newline='', encoding='utf-8')
    self.writer = csv.writer(self.file)
    self.writer.writerow(['Название', 'Автор','Цена со скидкой', 'Цена без скидки', 'Ссылка', 'Картинка'])    

  def close_spider(self, spider):
    self.file.close()

  def process_item(self, item, spider):
    self.writer.writerow([item['name'], item['author'], item['discountedprice'], item['fullprice'], item['link'], item['image']])
    return item

class LBSpider(scrapy.Spider):
  name = "Labirint parser"
  start_urls = ['https://www.labirint.ru/books/']  + ['https://www.labirint.ru/books/?page=' + str(i) for i in range(2,5)] 
  custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'DOWNLOAD_DELAY': 1,
      'ITEM_PIPELINES': {
        'labirint.LBPipeline': 300,
      }
  }

  def parse(self, response):
    selector = '.genres-carousel__container .genres-carousel__item'
    soup = BeautifulSoup(response.text, 'lxml')
    rows = soup.select(selector)
    for row in rows:
      cover = row.select(".product-title-link")
      names = row.select(".product")
      image = row.select('.book-img-cover')
      author = row.select('.product-author a')
      
      if len(cover) * len(names) * len(image) == 0:
        continue
      item = BookItem()
      item['name'] = names[0]['data-name']
      item['image'] = image[0]['src']
      item['discountedprice'] = names[0]['data-discount-price']
      item['fullprice'] = names[0]['data-price']
      item['link'] = cover[0]['href']
      if len(author) != 0:
        item['author'] = author[0]['title']
      else:
        item['author'] = 'N/A'
      yield item