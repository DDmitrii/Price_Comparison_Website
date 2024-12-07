from Bookparser import BookItem
import scrapy
from bs4 import BeautifulSoup

class LBSpider(scrapy.Spider):
  name = "Labirint parser"
  baselink = 'https://www.labirint.ru/books/'
  pagelink = 'https://www.labirint.ru/books/?page='
  start_urls = [baselink]
  custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'DOWNLOAD_DELAY': 1,
      'ITEM_PIPELINES': {
        'parser.CSVPipeline': 300,
      }
  }

  def set_pipeline(pipeline_name):
    LBSpider.custom_settings['ITEM_PIPELINES'] = {
        pipeline_name: 300,
    }

  def set_pages_amount(n):
    if n <= 1:
      LBSpider.start_urls = [LBSpider.baselink]
    else:
      LBSpider.start_urls = [LBSpider.baselink] + [LBSpider.pagelink + str(i) for i in range(2,n+1)]

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
      item['websitename'] = 'Labirint'
      item['name'] = names[0]['data-name']
      item['image'] = image[0]['src']
      item['discountedprice'] = names[0]['data-discount-price']
      item['fullprice'] = names[0]['data-price']
      item['link'] = 'https://www.labirint.ru' + cover[0]['href']
      if len(author) != 0:
        item['author'] = author[0]['title']
      else:
        item['author'] = 'N/A'
      yield item