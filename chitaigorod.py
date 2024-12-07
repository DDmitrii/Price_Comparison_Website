from bookitem import BookItem
import scrapy
from bs4 import BeautifulSoup

class CGSpider(scrapy.Spider):
  name = "chitaigorod parser"
  querylink = 'https://www.chitai-gorod.ru/search?phrase='
  baselink = 'https://www.chitai-gorod.ru/catalog/books-18030'
  pagelink = 'https://www.chitai-gorod.ru/catalog/books-18030?page='
  start_urls = [baselink]
  custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'DOWNLOAD_DELAY': 1,
      'ITEM_PIPELINES': {
        'parser.CSVPipeline': 300,
      }
  }

  def set_pipeline(pipeline_name):
    CGSpider.custom_settings['ITEM_PIPELINES'] = {
        pipeline_name: 300,
    }
  def set_query(query):
    CGSpider.start_urls = [CGSpider.querylink + query.replace(' ', "%20")]
  def set_pages_amount(n):
    if n <= 1:
      CGSpider.start_urls = [CGSpider.baselink]
    else:
      CGSpider.start_urls = [CGSpider.baselink] + [CGSpider.pagelink + str(i) for i in range(2,n+1)]

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