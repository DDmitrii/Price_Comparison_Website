from parser import BookItem
import csv
import scrapy
from bs4 import BeautifulSoup

class CGPipeline:
  def open_spider(self, spider):
    self.file = open('CG.csv', 'w', newline='', encoding='utf-8')
    self.writer = csv.writer(self.file)
    self.writer.writerow(['Название', 'Автор','Цена со скидкой', 'Цена без скидки', 'Ссылка', 'Картинка'])

  def close_spider(self, spider):
    self.file.close()

  def process_item(self, item, spider):
    self.writer.writerow([item['name'], item['author'], item['discountedprice'], item['fullprice'], item['link'], item['image']])
    return item

class CGSpider(scrapy.Spider):
  name = "chitaigorod parser"
  start_urls = ['https://www.chitai-gorod.ru/catalog/books-18030']# + ['https://www.chitai-gorod.ru/catalog/books-18030?page=' + str(i) for i in range(1,10)]
  custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'DOWNLOAD_DELAY': 1,
      'ITEM_PIPELINES': {
        'chitaigorod.CGPipeline': 300,
      }
  }

  def parse(self, response):
    selector = '.products-list .product-card'
    soup = BeautifulSoup(response.text, 'lxml')
    rows = soup.select(selector)
    parsed = 0
    for row in rows:
      links = row.select(".product-card__picture")
      images = row.select(".product-picture__img")
      author = row.select(".product-title__author")
      if len(links) * len(images) * len(author) == 0:
        continue
      print(row.known_xml)
      if 'data-chg-product-old-price' not in row.attrs:
        continue
      item = BookItem()
      item['name'] = row['data-chg-product-name']
      item['image'] = 'nolink'
      item['fullprice'] = row['data-chg-product-old-price']
      item['author'] = author[0].text.strip()
      if 'data-chg-product-price' in row.attrs:
        item['discountedprice'] = row['data-chg-product-price']
      else:
        item['discountedprice'] = item['fullprice']
      item['link'] = "chitai-gorod.ru/" + links[0]['href']
      parsed += 1
      yield item
    print(f"sucessfuly parsed {parsed} books")