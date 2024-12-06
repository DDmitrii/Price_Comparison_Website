from parser import BookItem
import csv
import scrapy
from bs4 import BeautifulSoup

class MIFPipeline:
  def open_spider(self, spider):
    self.file = open('MIF.csv', 'w', newline='', encoding='utf-8')
    self.writer = csv.writer(self.file)
    self.writer.writerow(['Название', 'Автор','Цена со скидкой', 'Цена без скидки', 'Ссылка', 'Картинка'])    

  def close_spider(self, spider):
    self.file.close()

  def process_item(self, item, spider):
    self.writer.writerow([item['name'], item['author'], item['discountedprice'], item['fullprice'], item['link'], item['image']])
    return item

class MIFSpider(scrapy.Spider):
  name = "mann-ivanov-ferber parser"
  start_urls = ['https://www.mann-ivanov-ferber.ru/catalog/']
  custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'DOWNLOAD_DELAY': 1,
      'ITEM_PIPELINES': {
        'mif.MIFPipeline': 300,
      }
  }

  def parse(self, response):
    selector = '.sc-724e57a8-0 .sc-62bfb586-0'
    soup = BeautifulSoup(response.text, 'lxml')
    rows = soup.select(selector)
    for row in rows:
      links = row.select(".jBHpRW")
      names = row.select(".jBHpRW .sc-d90e5ee2-3")
      prices = row.select(".sc-29c909f0-0")

      if len(links) * len(names) * len(prices) == 0:
        continue
      item = BookItem()
      item['name'] = names[0]['alt']
      item['image'] = names[0]['src']
      item['discountedprice'] = prices[0].text
      item['fullprice'] = prices[1].text
      item['link'] = [a['href'] for a in links][0]
      item['author'] = 'N/A'
      yield item