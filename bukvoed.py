from Bookparser import BookItem
import scrapy
from bs4 import BeautifulSoup

class BukvoedSpider(scrapy.Spider):
  name = "Labirint parser"
  baselink = 'https://www.bookvoed.ru/catalog'
  pagelink = 'https://www.bookvoed.ru/catalog?page='
  start_urls = [baselink]
  custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'DOWNLOAD_DELAY': 1,
      'ITEM_PIPELINES': {
        'parser.CSVPipeline': 300,
      }
  }

  def set_pipeline(pipeline_name):
    BukvoedSpider.custom_settings['ITEM_PIPELINES'] = {
        pipeline_name: 300,
    }

  def set_pages_amount(n):
    if n <= 1:
      BukvoedSpider.start_urls = [BukvoedSpider.baselink]
    else:
      BukvoedSpider.start_urls = [BukvoedSpider.baselink] + [BukvoedSpider.pagelink + str(i) for i in range(2,n+1)]

  def parse(self, response):
    selector = '.product-list .product-card'
    soup = BeautifulSoup(response.text, 'lxml')
    rows = soup.select(selector)
    for row in rows:
      link = row.select('.product-card__image-link')
      author = row.select('.product-description__author .ui-comma-separated-links__tag')
      image = row.select('img')
      
      if len(link) * len(image) == 0:
        continue
      item = BookItem()
      item['websitename'] = 'Bukvoed'
      item['name'] = row['data-product-name']
      item['image'] = image[0]['src'][2:]
      item['discountedprice'] = row['data-product-price-discounted'][:-5]
      item['fullprice'] = row['data-product-price-total'][:-5]
      item['link'] = 'https://www.bookvoed.ru' + link[0]['href']
      if len(author) != 0:
        item['author'] = ''.join([i.text + "," for i in author])[:-1]
      else:
        item['author'] = 'N/A'
      yield item