from parser import BookItem
import scrapy
from bs4 import BeautifulSoup

class MIFSpider(scrapy.Spider):
  name = "mann-ivanov-ferber parser"
  start_urls = ['https://www.mann-ivanov-ferber.ru/catalog/']
  custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'DOWNLOAD_DELAY': 1,
      'ITEM_PIPELINES': {
        'parser.CSVPipeline': 300,
      }
  }

  def set_pipeline(pipeline_name):
    MIFSpider.custom_settings['ITEM_PIPELINES'] = {
        pipeline_name: 300,
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